from rest_framework import serializers
from ..models import Answer


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'user', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = ['user', 'date_created', 'date_modified']
