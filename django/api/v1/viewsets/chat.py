from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from api.models import Chat
from ..serializers import ChatSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Chat.objects.all()
        room = self.request.query_params.get('room', default=None)
        if room is not None:
            queryset = queryset.filter(room__pk=room)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
