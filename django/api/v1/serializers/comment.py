from rest_framework import serializers
from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'target', 'content', 'date_created']
        read_only_fields = ['pk', 'date_created']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'user', 'target', 'content', 'date_created', 'date_modified']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'user', 'target', 'content', 'date_created', 'date_modified']


class CommentFieldMixin(serializers.Serializer):
    comments = CommentListSerializer(source='comment_set', many=True, read_only=True)
