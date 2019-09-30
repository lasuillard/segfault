import logging
from rest_framework import status
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels import layers
from core.models import Notification
from ..serializers import NotificationWebSocketSerializer

logger = logging.getLogger(__name__)
GLOBAL_NOTIFICATION_CHANNEL = 'GLOBAL-NOTIFICATION-CHANNEL-GROUP'


async def send_notification(notification):
    if isinstance(notification, Notification):
        channel_layer = layers.get_channel_layer()
        for user in notification.users.all():
            if not hasattr(user, 'avatar'):
                continue

            channel_group = user.avatar.get_channel_group()
            await channel_layer.group_send(
                channel_group,
                {
                    'type': 'notification.send',
                    'message': NotificationWebSocketSerializer(notification).data,
                }
            )


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.user = None
        self.channel_group = None
        super(NotificationConsumer, self).__init__(*args, **kwargs)

    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close(code=status.HTTP_401_UNAUTHORIZED)  # Unauthorized
            return

        self.channel_group = self.user.avatar.get_channel_group()
        await self.channel_layer.group_add(GLOBAL_NOTIFICATION_CHANNEL, self.channel_name)
        await self.channel_layer.group_add(self.channel_group, self.channel_name)
        await self.accept(subprotocol='access_token')  # OK

    async def disconnect(self, code):
        await self.channel_layer.group_discard(GLOBAL_NOTIFICATION_CHANNEL, self.channel_name)
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)

    async def notification_send(self, event):
        message = event['message']
        await self.send_json(message)
