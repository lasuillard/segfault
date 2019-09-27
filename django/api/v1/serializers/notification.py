from rest_framework import serializers
from core.models import Notification
from .user import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['level', 'message', 'extra_data', 'date_created']
        read_only_fields = ['date_created']


class NotificationListSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Notification
        fields = ['level', 'message', 'extra_data', 'date_created']


class NotificationDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Notification
        fields = ['users', 'level', 'message', 'extra_data', 'date_created']
