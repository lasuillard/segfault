from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from core.models import Notification
from api.permissions import IsAdminUser, IsRelatedUser
from ..serializers import (
    NotificationSerializer, NotificationListSerializer, NotificationAdminListSerializer,
    NotificationDetailSerializer, NotificationAdminDetailSerializer
)

User = get_user_model()


class NotificationViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):

    def get_serializer_class(self):
        # for admin
        if self.request.user and self.request.user.is_staff:
            if self.action == 'list':
                return NotificationAdminListSerializer
            elif self.action == 'retrieve':
                return NotificationAdminDetailSerializer

        # for users
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'retrieve':
            return NotificationDetailSerializer

        return NotificationSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'destroy']:
            permissions = [IsRelatedUser | IsAdminUser]
        else:
            permissions = [IsAdminUser]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Notification.objects.all()

        return queryset

    def perform_destroy(self, instance):
        instance.mark_as_read(self.request.user)
