from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from core.models import Chat
from api.permissions import IsAdminUser, IsOwner
from ..serializers import ChatSerializer, ChatListSerializer, ChatDetailSerializer

User = get_user_model()


class ChatViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    API for chat resources

    avatar, exact match for primary key or case-insensitive partial match for display name
    room: exact match for room primary key or case-insensitive partial match for room name
    content, case in-sensitive partial match for content
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return ChatListSerializer
        elif self.action == 'retrieve':
            return ChatDetailSerializer

        return ChatSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsOwner | IsAdminUser, ]
        else:
            permissions = [IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Chat.objects.order_by('-date_created')
        query_params = self.request.query_params

        # avatar, exact match for primary key or case-insensitive partial match for display name
        avatar = query_params.get('avatar')
        if avatar:
            try:
                avatar = int(avatar)
                queryset = queryset.filter(user__avatar__pk=avatar)
            except ValueError:
                queryset = queryset.filter(user__avatar__display_name__icontains=avatar)

        # room, exact match for room primary key or case-insensitive partial match for room name
        room = query_params.get('room')
        if room:
            try:
                room = int(room)
                queryset = queryset.filter(room__pk=room)
            except ValueError:
                queryset = queryset.filter(room_name__icontains=room)

        # content, case in-sensitive partial match for content
        content = query_params.get('content')
        queryset = queryset.filter(content__icontains=content) if content else queryset

        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
