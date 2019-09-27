from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAdminUser
from core.models import Notification
from api.permissions import IsRelatedUser
from ..serializers import NotificationSerializer, NotificationListSerializer, NotificationDetailSerializer

User = get_user_model()


class NotificationViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsRelatedUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'retrieve':
            return NotificationDetailSerializer

        return NotificationSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permissions = [IsRelatedUser]
        else:
            permissions = [IsAdminUser]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Notification.objects.all()

        return queryset
