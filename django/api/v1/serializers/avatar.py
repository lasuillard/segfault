from rest_framework import serializers
from core.models import Avatar


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ['pk', 'profile_image', 'display_name', 'introduce_message', 'extra_data', 'date_modified']
        read_only_fields = ['pk', 'date_modified']


class AvatarListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:avatar-detail')

    class Meta:
        model = Avatar
        fields = ['url', 'profile_image', 'display_name']


class AvatarDetailSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:v1:user-detail', read_only=True)

    class Meta:
        model = Avatar
        fields = ['pk', 'user', 'profile_image', 'display_name', 'introduce_message', 'extra_data', 'date_modified']


class AvatarFieldMixin(serializers.Serializer):
    """
        This mixins is for using avatar instance indirectly via user instance
    """
    avatar = AvatarSerializer(source='user.avatar', read_only=True)
