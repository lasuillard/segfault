from rest_framework import serializers
from ..models import Avatar


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['pk', 'profile_image', 'display_name', 'introduce_message', 'user_data', 'date_modified']
        read_only_fields = ['pk', 'date_modified']
