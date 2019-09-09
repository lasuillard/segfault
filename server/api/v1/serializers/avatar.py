from rest_framework import serializers
from api.models import Avatar


class AvatarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Avatar
        fields = ['url', 'profile_image', 'display_name']
        read_only_fields = ['profile_image', 'display_name']


class AvatarDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Avatar
        fields = ['pk', 'user', 'profile_image', 'display_name', 'introduce_message', 'user_data', 'date_modified']
        read_only_fields = ['user', 'date_modified']
