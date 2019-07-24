from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Avatar,
    Fragment,
    Answer,
    Comment,
    Vote,
    ChatRoom,
    Chat,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['pk', 'user', 'profile_image', 'display_name', 'introduce_message', 'date_modified']
        read_only_fields = ['id', 'user', 'date_modified']


class FragmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fragment
        fields = ['pk', 'user', 'title', 'content', 'tags', 'is_closed', 'date_created', 'date_modified']
        read_only_fields = ['id', 'user', 'date_created', 'date_modified']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['pk', 'user', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = ['user', 'target', 'date_created', 'date_modified']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'parent', 'user', 'target', 'content', 'date_created', 'date_modified']
        read_only_fields = ['parent', 'user', 'target', 'date_created', 'date_modified']
        depth = 1


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['pk', 'user', 'target', 'rating']
        read_only_fields = ['user', 'target']


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['pk', 'name', 'users', 'date_created', 'date_modified']
        read_only_fields = ['users', 'date_created', 'date_modified']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['pk', 'user', 'room', 'content', 'date_created', 'date_modified']
        read_only_fields = ['user', 'room', 'date_created', 'date_modified']
