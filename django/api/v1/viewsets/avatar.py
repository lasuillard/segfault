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
    API for avatar resources

    name: case-insensitive partial match for display name
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
        queryset = Avatar.objects.order_by('display_name')
        query_params = self.request.query_params

        # name, case-insensitive partial match for display name
        name = query_params.get('name')
        queryset = queryset.filter(display_name__icontains=name) if name else queryset

        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
