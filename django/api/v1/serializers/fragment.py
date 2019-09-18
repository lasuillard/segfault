from rest_framework import serializers
from api.models import Fragment
from .avatar import AvatarFieldMixin
from .answer import AnswerFieldMixin
from .comment import CommentFieldMixin
from .vote import VoteFieldMixin


class FragmentSerializer(AvatarFieldMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')
    count_answer = serializers.IntegerField(source='get_answer_count', read_only=True)
    count_comment = serializers.IntegerField(source='get_comment_count', read_only=True)
    count_vote = serializers.IntegerField(source='get_vote_count', read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Fragment
        fields = ['url', 'avatar', 'title', 'tags', 'status',
                  'count_answer', 'count_comment', 'count_vote', 'average_rating', 'date_created']
        read_only_fields = []


class FragmentDetailSerializer(AvatarFieldMixin, AnswerFieldMixin, CommentFieldMixin, VoteFieldMixin,
                               serializers.ModelSerializer):

    class Meta:
        model = Fragment
        fields = [
            'pk', 'avatar', 'title', 'content', 'tags', 'status', 'date_created', 'date_modified', 'date_closed',
            'answers', 'comments', 'votes'
        ]
        read_only_fields = []
