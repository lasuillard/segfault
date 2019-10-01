from rest_framework import serializers
from core.models import Room
from api.mixins import ReadOnlySerializerMixin


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['pk', 'name', 'date_created', 'date_modified']


class RoomListSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['pk', 'user', 'name', 'date_created', 'date_modified']


class RoomDetailSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['pk', 'user', 'name', 'date_created', 'date_modified']
