from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from core.models import Room
from ..serializers import RoomSerializer, RoomListSerializer, RoomDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class RoomViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        elif self.action == 'retrieve':
            return RoomDetailSerializer

        return RoomSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Room.objects.all()
