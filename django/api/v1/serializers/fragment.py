from rest_framework import serializers
from core.models import Fragment, Tag
from api.mixins import ReadOnlySerializerMixin
from .avatar import AvatarFieldMixin
from .answer import AnswerFieldMixin
from .comment import CommentFieldMixin
from .vote import VoteFieldMixin
from .tag import TagListSerializer


class FragmentSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Fragment
        fields = ['pk', 'title', 'content', 'tags', 'date_created', 'date_modified']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        fragment = super().create(validated_data)
        fragment.tags.set(Tag.objects.get_or_create_from_string(tags))
        return fragment

    def update(self, instance, validated_data):
        # i think there MUST BE BETTER way to do these kind of job...
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.tags.set(
            Tag.objects.get_or_create_from_string(validated_data.pop('tags', instance.tags))
        )
        instance.save()
        return instance


class FragmentListSerializer(AvatarFieldMixin, ReadOnlySerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:fragment-detail')
    tags = TagListSerializer(many=True)
    count_answer = serializers.IntegerField(source='get_answer_count', read_only=True)
    count_comment = serializers.IntegerField(source='get_comment_count', read_only=True)
    count_vote = serializers.IntegerField(source='get_vote_count', read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Fragment
        fields = ['pk', 'url', 'avatar', 'title', 'tags', 'status',
                  'count_answer', 'count_comment', 'count_vote', 'average_rating', 'date_created']


class FragmentDetailSerializer(AvatarFieldMixin, AnswerFieldMixin, CommentFieldMixin, VoteFieldMixin,
                               ReadOnlySerializerMixin, serializers.ModelSerializer):
    tags = TagListSerializer(many=True)

    class Meta:
        model = Fragment
        fields = [
            'pk', 'avatar', 'title', 'content', 'tags', 'status', 'answers', 'comments', 'votes',
            'date_created', 'date_modified', 'date_closed'
        ]
