from rest_framework import serializers
from api.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['pk', 'user', 'target', 'rating']
        read_only_fields = []


class VoteDetailSerializer(serializers.ModelSerializer):
    pass


class VoteFieldMixin(serializers.Serializer):
    votes = VoteSerializer(source='vote_set', many=True, read_only=True)
