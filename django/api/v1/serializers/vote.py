from rest_framework import serializers
from core.models import Vote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'target', 'rating']
        read_only_fields = ['pk', 'user']


class VoteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'user', 'target', 'rating']


class VoteDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['pk', 'user', 'target', 'rating']


class VoteFieldMixin(serializers.Serializer):
    votes = VoteSerializer(source='vote_set', many=True, read_only=True)
