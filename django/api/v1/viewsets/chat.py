from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from core.models import Chat
from ..serializers import ChatSerializer, ChatListSerializer, ChatDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class ChatViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatListSerializer
        elif self.action == 'retrieve':
            return ChatDetailSerializer

        return ChatSerializer

    def get_queryset(self):
        queryset = Chat.objects.all()
        room = self.request.query_params.get('room', default=None)
        if room is not None:
            queryset = queryset.filter(room__pk=room)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
