from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from core.models import Avatar
from api.permissions import IsAdminUser, IsOwner
from ..serializers import AvatarSerializer, AvatarListSerializer, AvatarDetailSerializer

User = get_user_model()


class AvatarViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    """
    API for avatar object

    - Supported list filters:
    name: filter queries by display name of avatar, case in-sensitive partial match.
    """

    def get_serializer_class(self):
        if self.action == 'list':
            return AvatarListSerializer
        elif self.action == 'retrieve':
            return AvatarDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return AvatarSerializer

        return None

    def get_permissions(self):
        if self.action in ['list']:
            permissions = [AllowAny, ]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsOwner | IsAdminUser, ]
        else:
            permissions = [IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Avatar.objects.all()
        name = self.request.query_params.get('name', default=None)
        if name is not None:
            queryset = queryset.filter(display_name__icontains=name)

        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
