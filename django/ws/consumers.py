from django.core.exceptions import ValidationError
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import Room, Chat
from .serializers import ChatWebSocketSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.room = None
        self.user = None
        self.channel_group = None
        super(ChatConsumer, self).__init__(*args, **kwargs)

    async def connect(self):
        try:
            room_id = self.scope['url_route']['kwargs']['id']
            self.room = await database_sync_to_async(Room.objects.get)(pk=room_id)
            # Authenticate incoming request
            self.user = self.scope['user']
            if not self.user.is_authenticated:
                await self.close(code=401)  # Unauthorized

            self.channel_group = str(self.room.channel_group)  # channel_group is uuid4 field
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
            await self.channel_layer.group_send(
                self.channel_group,
                {
                    'type': 'chat.broadcast',
                    'message': await self.get_serialized_chat_data(data=content)
                }
            )
        except ValidationError:
            pass

    async def chat_broadcast(self, event):
        message = event['message']
        await self.send_json(message)

    @database_sync_to_async
    def get_serialized_chat_data(self, data):
        serializer = ChatWebSocketSerializer(
            Chat.objects.create(user=self.user, room=self.room, **data)
        )
        if serializer.is_valid():
            return serializer.data
