from django.urls import path
from .consumers import ChatConsumer, NotificationConsumer

app_name = 'ws'

websocket_urlpatterns = [
    path('ws/chat/<int:room_id>/', ChatConsumer, name='chat'),
    path('ws/notification/', NotificationConsumer, name='notification')
]
