from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from ..serializers import UserSerializer, UserDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer

        return UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', default=None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)

        return queryset
