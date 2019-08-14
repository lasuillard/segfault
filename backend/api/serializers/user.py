from django.contrib.auth import get_user_model
from rest_framework import serializers
from .avatar import AvatarSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = User
        fields = ['email', 'avatar']
        read_only_fields = ['email', 'avatar']


class UserDetailSerializer(serializers.ModelSerializer):
    """
        it overrides django-rest-auth UserDetailsSerializer with custom settings

        url: /rest-auth/user/
    """
    avatar = AvatarSerializer()

    class Meta:
        model = User
        fields = ['email', 'avatar']
        read_only_fields = ['email', 'avatar']
