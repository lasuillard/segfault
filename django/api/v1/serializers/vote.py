from rest_framework import serializers
from core.models import Vote
from api.mixins import ReadOnlySerializerMixin
from ..serializers import AvatarFieldMixin


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'target', 'rating', 'date_created', 'date_modified']


class VoteListSerializer(AvatarFieldMixin, ReadOnlySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'avatar', 'target', 'rating', 'date_created', 'date_modified']


class VoteDetailSerializer(VoteListSerializer):
    pass


class VoteFieldMixin(serializers.Serializer):
    votes = VoteListSerializer(source='vote_set', many=True, read_only=True)
