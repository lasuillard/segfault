from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from core.auth import TokenAuthMiddlewareStack
from ws.routing import websocket_urlpatterns
from ws.consumers import NotificationConsumer, ChatConsumer

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
    # for worker
    'channel': ChannelNameRouter({
        'notification': NotificationConsumer,
        'chat': ChatConsumer
    })
})
