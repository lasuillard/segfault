import logging
from django.core.exceptions import ValidationError
from rest_framework import status
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Room, Chat
from ..serializers import ChatWebSocketSerializer

logger = logging.getLogger()


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.room = None
        self.user = None
        self.channel_group = None
        super(ChatConsumer, self).__init__(*args, **kwargs)

    async def connect(self):
        try:
            # Authenticate incoming request
            self.user = self.scope['user']
            logger.debug(
                'Incoming connection for room {} by user {}'.format(
                    self.scope['url_route']['kwargs']['room_id'],
                    self.user
                )
            )
            if not self.user.is_authenticated:
                await self.close(code=status.HTTP_401_UNAUTHORIZED)  # Unauthorized
                logger.info(f'Rejected user:{self.user} connection for room:{self.room}')
                return

            self.room = await self.get_room()
            self.channel_group = self.room.get_channel_group()  # channel_group is uuid4 field
            await self.channel_layer.group_add(self.channel_group, self.channel_name)
            await self.accept(subprotocol='access_token')  # OK
            logger.info(f'Accepted user:{self.user}')

        except Room.DoesNotExist as e:
            await self.close(code=status.HTTP_400_BAD_REQUEST)  # Bad Request
            logger.warning(f'Cannot find room for chat socket: {e}')

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)
        logger.info(f'Disconnected user {self.user} from {self.room.id}')

    async def receive_json(self, content, **kwargs):
        try:
            chat = await self.get_chat_instance(data=content)
            await self.channel_layer.group_send(
                self.channel_group,
                {
                    'type': 'chat.broadcast',
                    'message': ChatWebSocketSerializer(chat).data
                }
            )
            logger.debug(f'Received and processed chat:{chat}')
        except ValidationError as e:
            logger.info(f'Received content:{content} could not pass validation: {e}')

    async def chat_broadcast(self, event):
        message = event['message']
        await self.send_json(message)
        logger.debug(f'Sending message to user:{self.user}')

    @database_sync_to_async
    def get_room(self):
        room_id = self.scope['url_route']['kwargs']['id']
        return Room.objects.get(pk=room_id)

    @database_sync_to_async
    def get_chat_instance(self, data):
        return Chat.objects.create(user=self.user, room=self.room, **data)
