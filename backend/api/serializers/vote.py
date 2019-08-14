from rest_framework import serializers
from ..models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['pk', 'user', 'target', 'rating']
        read_only_fields = ['pk', 'user', 'target']
