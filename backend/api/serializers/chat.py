from rest_framework import serializers
from ..models import ChatRoom, Chat


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['pk', 'name', 'users', 'date_created', 'date_modified']
        read_only_fields = ['pk', 'users', 'date_created', 'date_modified']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk', 'user', 'room', 'content', 'date_created', 'date_modified']
        read_only_fields = ['pk', 'user', 'room', 'date_created', 'date_modified']
