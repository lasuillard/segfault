from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from core.models import Room
from ..serializers import RoomSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
