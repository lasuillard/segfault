from rest_framework import serializers
from api.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'user', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = ['user', 'date_created', 'date_modified']
        depth = 1
