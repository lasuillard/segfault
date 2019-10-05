from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Answer
from api.permissions import IsAdminUser, IsOwner
from ..serializers import AnswerSerializer, AnswerListSerializer, AnswerDetailSerializer

User = get_user_model()


class AnswerViewSet(ModelViewSet):
    """
    API for Answer object

    - Supported filters:
    by: id or name of avatar. exact match for id, case in-sensitive partial match for name.
    target: fragment id, exact match.
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
        queryset = Answer.objects.all()
        by = self.request.query_params.get('by', default=None)
        if by is not None:
            try:
                queryset = queryset.filter(user__avatar__pk=by)
            except ValueError:
                queryset = queryset.filter(user__avatar__display_name__icontains=by)

        target = self.request.query_params.get('target', default=None)
        if target is not None:
            try:
                queryset = queryset.filter(target__pk=target)
            except ValueError:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
