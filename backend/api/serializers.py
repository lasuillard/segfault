from rest_framework import serializers
from .models import Avatar


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('id', 'user', 'profile_image', 'display_name', 'introduce_message')
