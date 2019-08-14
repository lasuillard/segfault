from rest_framework import serializers
from ..models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'user', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = ['pk', 'user', 'target', 'date_created', 'date_modified']
