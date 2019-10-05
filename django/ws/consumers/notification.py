import logging
from rest_framework import status
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)

GLOBAL_NOTIFICATION_CHANNEL = 'GLOBAL-NOTIFICATION-CHANNEL-GROUP'


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.user = None
        self.channel_group = None
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.user = self.scope['user']
        logger.info('Incoming connection request for notification service: {}'.format(self.user))
        if not self.user.is_authenticated:
            logger.info('Rejected connection request because of authorization failure: {}'.format(self.user))
            await self.close(code=status.HTTP_401_UNAUTHORIZED)  # Unauthorized
            return

        logger.info('Accepted connection request: {}'.format(self.user))
        self.channel_group = self.user.avatar.get_channel_group()
        await self.channel_layer.group_add(GLOBAL_NOTIFICATION_CHANNEL, self.channel_name)
        await self.channel_layer.group_add(self.channel_group, self.channel_name)
        await self.accept(subprotocol='access_token')  # OK

    async def disconnect(self, code):
        logger.info('Disconnected user: {}'.format(self.user))
        await self.channel_layer.group_discard(GLOBAL_NOTIFICATION_CHANNEL, self.channel_name)
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        logger.warning('Received data but this is read-only web socket: {}'.format(content))

    async def notification_send(self, event):
        logger.info('Sending notification for user: {}'.format(self.user))
        message = event['message']
        await self.send_json(message)
