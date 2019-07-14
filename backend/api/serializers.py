from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Avatar


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('id', 'user', 'profile_image', 'display_name', 'introduce_message')
