from rest_framework import serializers
from core.models import Notification
from .user import UserListSerializer


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['level', 'message', 'extra_data', 'date_created']
        read_only_fields = ['date_created']


class NotificationListSerializer(serializers.ModelSerializer):
    users = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = ['users', 'level', 'message', 'extra_data', 'date_created']


class NotificationDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['level', 'message', 'extra_data', 'date_created']
