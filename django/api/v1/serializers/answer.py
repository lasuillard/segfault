from rest_framework import serializers
from api.models import Answer
from .avatar import AvatarFieldMixin


class AnswerSerializer(serializers.ModelSerializer, AvatarFieldMixin):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:answer-detail')
    target = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')

    class Meta:
        model = Answer
        fields = ['url', 'avatar', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = []


class AnswerDetailSerializer(serializers.ModelSerializer, AvatarFieldMixin):
    target = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')

    class Meta:
        model = Answer
        fields = ['pk', 'avatar', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = []


class AnswerFieldMixin(serializers.Serializer):
    answers = AnswerSerializer(source='answer_set', many=True, read_only=True)
