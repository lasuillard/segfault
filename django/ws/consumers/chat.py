from django.core.exceptions import ValidationError
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Room, Chat
from ..serializers import ChatWebSocketSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.room = None
        self.user = None
        self.channel_group = None
        super(ChatConsumer, self).__init__(*args, **kwargs)

    async def connect(self):
        try:
            room_id = self.scope['url_route']['kwargs']['id'] # merge this two line into separate method
            self.room = await database_sync_to_async(Room.objects.get)(pk=room_id) # merge
            # Authenticate incoming request
            self.user = self.scope['user']
            if not self.user.is_authenticated:
                await self.close(code=401)  # Unauthorized
                return

            self.channel_group = self.room.get_channel_group()  # channel_group is uuid4 field
            await self.channel_layer.group_add(self.channel_group, self.channel_name)
            await self.accept(subprotocol='access_token')  # OK

        except KeyError:
            await self.close(code=500)  # Internal server error

        except Room.DoesNotExist:
            await self.close(code=400)  # Bad Request

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)

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
        except ValidationError:
            pass

    async def chat_broadcast(self, event):
        message = event['message']
        await self.send_json(message)

    @database_sync_to_async
    def get_chat_instance(self, data):
        return Chat.objects.create(user=self.user, room=self.room, **data)
