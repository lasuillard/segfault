from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from api.permissions import IsAdminUser, IsOwner
from ..serializers import UserSerializer, UserListSerializer, UserDetailSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            permissions = [IsAdminUser]
        else:
            permissions = [IsOwner | IsAdminUser]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', default=None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)

        return queryset
