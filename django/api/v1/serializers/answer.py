from rest_framework import serializers
from core.models import Answer
from .avatar import AvatarFieldMixin


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['pk', 'target', 'content', 'date_created']
        read_only_fields = ['pk', 'date_created']


class AnswerListSerializer(serializers.ModelSerializer, AvatarFieldMixin):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:answer-detail')
    target = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')

    class Meta:
        model = Answer
        fields = ['url', 'avatar', 'target', 'content', 'date_created', 'date_modified']


class AnswerDetailSerializer(serializers.ModelSerializer, AvatarFieldMixin):
    target = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')

    class Meta:
        model = Answer
        fields = ['pk', 'avatar', 'target', 'content', 'date_created', 'date_modified']


class AnswerFieldMixin(serializers.Serializer):
    answers = AnswerListSerializer(source='answer_set', many=True, read_only=True)
