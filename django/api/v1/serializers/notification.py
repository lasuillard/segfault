from rest_framework import serializers
from core.models import Notification
from api.mixins import ReadOnlySerializerMixin
from .user import UserListSerializer


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['pk', 'title', 'body', 'extra_data', 'date_created']


class NotificationListSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:notification-detail')

    class Meta:
        model = Notification
        fields = ['pk', 'url', 'title', 'date_created']


class NotificationAdminListSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:notification-detail')
    users = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = ['pk', 'url', 'users', 'title', 'body', 'date_created']


class NotificationDetailSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['pk', 'title', 'body', 'extra_data', 'date_created']


class NotificationAdminDetailSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    users = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = ['pk', 'users', 'title', 'body', 'extra_data', 'date_created']
