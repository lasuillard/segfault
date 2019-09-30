from django.contrib.auth import get_user_model
from rest_framework import serializers
from .avatar import AvatarListSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username']
        read_only_fields = ['pk', 'username']


class UserListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:user-detail')
    avatar = AvatarListSerializer()

    class Meta:
        model = User
        fields = ['url', 'avatar']


class UserDetailSerializer(serializers.ModelSerializer):
    """
        it overrides django-rest-auth UserDetailsSerializer with custom settings
    """
    avatar = AvatarListSerializer()

    class Meta:
        model = User
        fields = ['pk', 'email', 'username', 'avatar']
