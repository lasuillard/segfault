from rest_framework import serializers
from api.models import Fragment
from .user import UserSerializer


class FragmentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    answer_count = serializers.IntegerField(source='get_answer_count', read_only=True)
    comment_count = serializers.IntegerField(source='get_comment_count', read_only=True)
    vote_count = serializers.IntegerField(source='get_vote_count', read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Fragment
        fields = ['url', 'user', 'title', 'tags', 'is_closed', 'answer_count',
                  'comment_count', 'vote_count', 'average_rating', 'date_created']
        read_only_fields = ['user', 'answer_count', 'comment_count', 'vote_count', 'average_rating', 'date_created']


class FragmentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Fragment
        fields = ['pk', 'user', 'title', 'content', 'tags', 'is_closed', 'date_created', 'date_modified']
        read_only_fields = ['user', 'date_created', 'date_modified']
