from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from api.models import Avatar
from ..serializers import AvatarSerializer, AvatarDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class AvatarViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
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

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
