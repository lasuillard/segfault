import logging
from django.core.exceptions import ValidationError
from rest_framework import status
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Room, Chat
from ..serializers import ChatWebSocketSerializer

logger = logging.getLogger()


class ChatConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def get_room(self):
        room_id = self.scope['url_route']['kwargs']['id']
        return Room.objects.get(pk=room_id)

    @database_sync_to_async
    def get_serialized_chat_data(self, data):
        logger.debug('Validating and serializing chat data: {}'.format(data))
        chat = Chat(user=self.user, room=self.room, **data)
        chat.full_clean()
        chat.save()
        chat = ChatWebSocketSerializer(chat).data
        return chat

    def __init__(self, *args, **kwargs):
        self.room = None
        self.user = None
        self.channel_group = None
        super().__init__(*args, **kwargs)

    async def connect(self):
        # Authenticate incoming request
        room_id = self.scope['url_route']['kwargs']['room_id'],
        self.user = self.scope['user']
        logger.info('Incoming connection request for room {} by user {}'.format(room_id, self.user))
        if not self.user.is_authenticated:
            logger.info('Rejected connection request for room {} because authorization has failed: {}'.format(
                room_id, self.user))
            await self.close(code=status.HTTP_401_UNAUTHORIZED)  # Unauthorized
            return

        try:
            self.room = await self.get_room()
        except Room.DoesNotExist:
            logger.warning('Rejected connection for room {} because it does not exist: {}'.format(room_id, self.user))
            await self.close(code=status.HTTP_400_BAD_REQUEST)
            return

        logger.info('Accepted user for room {}: {}'.format(room_id, self.user))
        self.channel_group = self.room.get_channel_group()  # channel_group is uuid4 field
        await self.channel_layer.group_add(self.channel_group, self.channel_name)
        await self.accept(subprotocol='access_token')  # OK

    async def disconnect(self, code):
        logger.info('Disconnected user {} from room {}'.format(self.user, self.room.pk))
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        try:
            data = await self.get_serialized_chat_data(data=content)
        except ValidationError:
            logger.warning('Sending error message in response to malformed data')
            await self.send_json({'error': 'could not send chat message. data is invalid.'})
            return
        except TypeError:
            logger.warning('Sending error message in response to malformed data')
            await self.send_json({'error': 'could not send chat message. data is malformed.'})
            return

        logger.debug('Broadcasting chat message to channel group: {}'.format(self.channel_group))
        await self.channel_layer.group_send(
            self.channel_group,
            {
                'type': 'chat.broadcast',
                'message': data
            }
        )

    async def chat_broadcast(self, event):
        logger.debug('Sending message to user: {}'.format(self.user))
        message = event['message']
        await self.send_json(message)
