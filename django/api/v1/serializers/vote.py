from rest_framework import serializers
from core.models import Vote
from api.mixins import ReadOnlySerializerMixin
from ..serializers import AvatarFieldMixin


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'target', 'rating', 'date_created', 'date_modified']

    def create(self, validated_data):
        vote, _ = Vote.objects.update_or_create(
            user=validated_data['user'],
            target=validated_data['target'],
            defaults={'rating': validated_data['rating']})
        return vote


class VoteListSerializer(AvatarFieldMixin, ReadOnlySerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'avatar', 'target', 'rating', 'date_created', 'date_modified']


class VoteDetailSerializer(VoteListSerializer):
    pass


class VoteFieldMixin(serializers.Serializer):
    votes = VoteListSerializer(source='vote_set', many=True, read_only=True)
