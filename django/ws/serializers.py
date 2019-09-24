from rest_framework import serializers
from api.models import Avatar, Chat
"""
/ws/serializers.py

define serializers independently from the ones that api-versioned.
it is strictly, narrowly designed to fit chat web socket consumers.
"""


class AvatarWebSocketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ['pk', 'profile_image', 'display_name']


class ChatWebSocketSerializer(serializers.ModelSerializer):
    avatar = AvatarWebSocketSerializer(source='user.avatar', read_only=True)

    class Meta:
        model = Chat
        fields = ['avatar', 'content', 'date_created']
