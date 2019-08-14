from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from ..models import Avatar
from ..serializers import AvatarSerializer
from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class AvatarViewSet(ModelViewSet):
    serializer_class = AvatarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Avatar.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
