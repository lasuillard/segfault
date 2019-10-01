from rest_framework import serializers
from core.models import Comment
from api.mixins import ReadOnlySerializerMixin
from ..serializers import AvatarFieldMixin


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'target', 'content', 'date_created', 'date_modified']


class CommentListSerializer(AvatarFieldMixin, ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'avatar', 'target', 'content', 'date_created', 'date_modified']


class CommentDetailSerializer(CommentListSerializer):
    pass


class CommentFieldMixin(serializers.Serializer):
    comments = CommentListSerializer(source='comment_set', many=True, read_only=True)
