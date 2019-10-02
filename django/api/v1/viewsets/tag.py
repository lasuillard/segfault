from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from core.models import Tag
from ..serializers import TagSerializer, TagListSerializer, TagDetailSerializer

User = get_user_model()


class TagViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return TagListSerializer
        elif self.action == 'retrieve':
            return TagDetailSerializer

        return TagSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permissions = [AllowAny, ]
        else:
            permissions = [IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Tag.objects.all()

        return queryset
