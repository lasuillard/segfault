from rest_framework import serializers
from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'user', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = ['user', 'date_created', 'date_modified']


class CommentDetailSerializer(serializers.ModelSerializer):
    pass


class CommentFieldMixin(serializers.Serializer):
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)
