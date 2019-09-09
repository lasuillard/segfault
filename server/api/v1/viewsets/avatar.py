from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from api.models import Avatar
from ..serializers import AvatarSerializer, AvatarDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class AvatarViewSet(ModelViewSet):
    serializer_class = AvatarSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ['head', 'options', 'get', 'put', 'patch']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AvatarDetailSerializer

        return AvatarSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Avatar.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user=user)

        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
