from channels.routing import ProtocolTypeRouter, URLRouter
from ws.routing import websocket_urlpatterns
from .auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
