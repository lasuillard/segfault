from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from core.models import Notification
from api.permissions import IsOwnerOrReadOnly
from ..serializers import NotificationSerializer

User = get_user_model()


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Notification.objects.all()

        return queryset
