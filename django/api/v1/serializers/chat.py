from rest_framework import serializers
from core.models import Chat
from api.mixins import ReadOnlySerializerMixin
from ..serializers import AvatarFieldMixin


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['pk', 'content', 'date_created', 'date_modified']


class ChatListSerializer(AvatarFieldMixin, ReadOnlySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['pk', 'avatar', 'room', 'content', 'date_created', 'date_modified']


class ChatDetailSerializer(ChatListSerializer):
    pass
