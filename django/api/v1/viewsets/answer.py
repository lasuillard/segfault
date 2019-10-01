from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Answer
from api.permissions import IsAdminUser, IsOwner
from ..serializers import AnswerSerializer, AnswerListSerializer, AnswerDetailSerializer

User = get_user_model()


class AnswerViewSet(ModelViewSet):

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
        queryset = Answer.objects.all()
        user = self.request.query_params.get('user', default=None)
        target = self.request.query_params.get('target', default=None)
        if user is not None:
            queryset = queryset.filter(user__username=user)

        if target is not None:
            queryset = queryset.filter(target__pk=target)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
