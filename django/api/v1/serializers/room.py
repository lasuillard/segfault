from rest_framework import serializers
from core.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['pk', 'name', 'users', 'date_created', 'date_modified']
        read_only_fields = ['users', 'date_created', 'date_modified']


class RoomDetailSerializer(serializers.ModelSerializer):
    pass
