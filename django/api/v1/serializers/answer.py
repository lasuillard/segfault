from rest_framework import serializers
from core.models import Answer
from api.mixins import ReadOnlySerializerMixin
from .avatar import AvatarFieldMixin
from .comment import CommentFieldMixin
from .vote import VoteFieldMixin


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['pk', 'target', 'content', 'date_created', 'date_modified']


class AnswerListSerializer(AvatarFieldMixin, ReadOnlySerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:answer-detail')
    target = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')

    class Meta:
        model = Answer
        fields = ['pk', 'url', 'avatar', 'target', 'content', 'date_created', 'date_modified']


class AnswerDetailSerializer(AvatarFieldMixin, CommentFieldMixin, VoteFieldMixin,
                             ReadOnlySerializerMixin, serializers.ModelSerializer):
    target = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')

    class Meta:
        model = Answer
        fields = ['pk', 'avatar', 'target', 'content', 'comments', 'votes', 'date_created', 'date_modified']


class AnswerFieldMixin(serializers.Serializer):
    answers = AnswerListSerializer(source='answer_set', many=True, read_only=True)
