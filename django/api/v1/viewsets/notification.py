from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from core.models import Notification
from api.permissions import IsAdminUser, IsRelatedUser
from ..serializers import NotificationSerializer, NotificationListSerializer, NotificationDetailSerializer

User = get_user_model()


class NotificationViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'retrieve':
            return NotificationDetailSerializer

        return NotificationSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permissions = [IsRelatedUser | IsAdminUser]
        else:
            permissions = [IsAdminUser]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Notification.objects.all()

        return queryset
