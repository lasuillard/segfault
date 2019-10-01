from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.permissions import IsAdminUser, IsOwner
from ..serializers import UserListSerializer, UserDetailSerializer

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer

        return None

    def get_permissions(self):
        if self.action == 'retrieve':
            permissions = [IsOwner | IsAdminUser]
        else:
            permissions = [IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', default=None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)

        return queryset
