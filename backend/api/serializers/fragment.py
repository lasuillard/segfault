from rest_framework import serializers
from ..models import Fragment


class FragmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fragment
        fields = ['pk', 'user', 'title', 'content', 'tags', 'is_closed', 'date_created', 'date_modified']
        read_only_fields = ['pk', 'user', 'date_created', 'date_modified']
