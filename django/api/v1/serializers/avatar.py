from rest_framework import serializers
from api.models import Avatar


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:avatar-detail')

    class Meta:
        model = Avatar
        fields = ['url', 'profile_image', 'display_name']
        read_only_fields = ['url', 'profile_image', 'display_name']


class AvatarDetailSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:v1:user-detail', read_only=True)

    class Meta:
        model = Avatar
        fields = ['pk', 'user', 'profile_image', 'display_name', 'introduce_message', 'extra_data', 'date_modified']
        read_only_fields = ['pk', 'user', 'date_modified']