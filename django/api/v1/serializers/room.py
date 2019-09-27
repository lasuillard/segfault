from rest_framework import serializers
from core.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['pk', 'name', 'date_created']
        read_only_fields = ['pk', 'date_created']


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['pk', 'user', 'name', 'date_created', 'date_modified']


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['pk', 'user', 'name', 'date_created', 'date_modified']
