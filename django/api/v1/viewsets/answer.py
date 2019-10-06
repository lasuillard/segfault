from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Answer
from api.permissions import IsAdminUser, IsOwner
from ..serializers import AnswerSerializer, AnswerListSerializer, AnswerDetailSerializer

User = get_user_model()


class AnswerViewSet(ModelViewSet):
    """
    API for answer resources

    avatar : exact match for avatar primary key or case-insensitive inclusion for display name
    target : exact match for fragment primary key
    content: case-insensitive partial match for content
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return AnswerListSerializer
        elif self.action == 'retrieve':
            return AnswerDetailSerializer

        return AnswerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny, ]
        elif self.action == 'create':
            permissions = [IsAuthenticated | IsAdminUser, ]
        else:
            permissions = [IsOwner | IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Answer.objects.order_by('-date_created')
        query_params = self.request.query_params

        # avatar, exact match for primary key or case-insensitive partial match for display name
        avatar = query_params.get('avatar')
        if avatar:
            try:
                avatar = int(avatar)
                queryset = queryset.filter(user__avatar__pk=avatar)
            except ValueError:
                queryset = queryset.filter(user__avatar__display_name__icontains=avatar)

        # target, exact match, primary key
        target = query_params.get('target')
        if target:
            try:
                target = int(target)
                queryset = queryset.filter(target__pk=target)
            except ValueError:
                pass

        # content, case-insensitive partial match for content
        content = query_params.get('content')
        queryset = queryset.filter(content__icontains=content) if content else queryset

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
