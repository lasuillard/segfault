from rest_framework import serializers
from core.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk', 'content', 'date_created']
        read_only_fields = ['pk', 'date_created']


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk', 'user', 'room', 'content', 'date_created', 'date_modified']


class ChatDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk', 'user', 'room', 'content', 'date_created', 'date_modified']
