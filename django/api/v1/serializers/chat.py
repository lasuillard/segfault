from rest_framework import serializers
from api.models import ChatRoom, Chat


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['pk', 'name', 'users', 'date_created', 'date_modified']
        read_only_fields = ['users', 'date_created', 'date_modified']


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    pass


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk', 'user', 'room', 'content', 'date_created', 'date_modified']
        read_only_fields = ['user', 'date_created', 'date_modified']


class ChatDetailSerializer(serializers.ModelSerializer):
    pass
