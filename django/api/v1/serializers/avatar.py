from rest_framework import serializers
from core.models import Avatar
from api.mixins import ReadOnlySerializerMixin


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ['pk', 'profile_image', 'display_name', 'introduce_message', 'extra_data', 'date_modified']


class AvatarListSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:avatar-detail')

    class Meta:
        model = Avatar
        fields = ['pk', 'url', 'profile_image', 'display_name']


class AvatarDetailSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:v1:user-detail', read_only=True)

    class Meta:
        model = Avatar
        fields = ['pk', 'user', 'profile_image', 'display_name', 'introduce_message', 'extra_data', 'date_modified']


class AvatarFieldMixin(serializers.Serializer):
    """
        This mixins is for using avatar instance indirectly via user instance
    """
    avatar = AvatarListSerializer(source='user.avatar', read_only=True)
