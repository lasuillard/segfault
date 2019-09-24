from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer, name='ws_chat')
]