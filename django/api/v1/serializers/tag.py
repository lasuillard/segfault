from rest_framework import serializers
from core.models import Tag
from api.mixins import ReadOnlySerializerMixin


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['pk', 'name', 'is_official', 'date_created', 'date_modified']


class TagListSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:tag-detail')
    count_related_contents = serializers.IntegerField(source='get_content_count', read_only=True)

    class Meta:
        model = Tag
        fields = ['pk', 'url', 'name', 'is_official', 'count_related_contents', 'date_created']


class TagDetailSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    count_related_contents = serializers.IntegerField(source='get_content_count', read_only=True)

    class Meta:
        model = Tag
        fields = ['pk', 'name', 'is_official', 'count_related_contents', 'date_created', 'date_modified']
