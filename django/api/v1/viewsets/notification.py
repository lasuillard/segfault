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
    """
    API for notification resources

    avatars: partial inclusion for display name with exact match, separated with comma(,)
    """
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
        queryset = Notification.objects.order_by('-date_created')
        query_params = self.request.query_params

        avatars = query_params.get('avatars')
        if avatars:
            avatars = avatars.split(',')
            queryset = queryset.filter(users__avatar__display_name__in=avatars)

        return queryset

    def perform_destroy(self, instance):
        instance.mark_as_read(self.request.user)
