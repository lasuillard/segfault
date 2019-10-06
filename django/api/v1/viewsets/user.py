from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.permissions import IsAdminUser, IsOwner
from ..serializers import UserListSerializer, UserDetailSerializer

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    """
    API for user resources

    name: partial match for username
    """
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

        # name, partial match for username
        name = self.request.query_params.get('name', default=None)
        queryset = queryset.filter(username__icontains=name) if name else queryset

        return queryset
