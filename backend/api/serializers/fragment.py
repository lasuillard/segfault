from rest_framework import serializers
from ..models import Fragment


class FragmentSerializer(serializers.ModelSerializer):
    answer_count = serializers.IntegerField(source='get_answer_count', read_only=True)
    comment_count = serializers.IntegerField(source='get_comment_count', read_only=True)
    vote_count = serializers.IntegerField(source='get_vote_count', read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Fragment
        fields = ['pk', 'user', 'title', 'tags', 'is_closed', 'answer_count', 'comment_count', 'vote_count', 'average_rating', 'date_created']
        read_only_fields = ['pk', 'answer_count', 'comment_count', 'vote_count', 'average_rating', 'date_created']


class FragmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fragment
        fields = ['pk', 'user', 'title', 'content', 'tags', 'is_closed', 'date_created', 'date_modified']
        read_only_fields = ['pk', 'user', 'date_created', 'date_modified']
