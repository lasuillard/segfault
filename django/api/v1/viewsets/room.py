from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Room
from api.permissions import IsAdminUser, IsOwner
from ..serializers import RoomSerializer, RoomListSerializer, RoomDetailSerializer

User = get_user_model()


class RoomViewSet(ModelViewSet):
    """
    API for chat room resources

    name: case-insensitive partial match for name
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        elif self.action == 'retrieve':
            return RoomDetailSerializer

        return RoomSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny, ]
        elif self.action == 'create':
            permissions = [IsAuthenticated | IsAdminUser, ]
        else:
            permissions = [IsOwner | IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Room.objects.all()
        query_params = self.request.query_params

        # name, case-insensitive partial match for name
        name = query_params.get('name')
        queryset = queryset.filter(name__icontains=name) if name else queryset

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
