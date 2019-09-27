from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from core.models import Answer
from api.permissions import IsOwnerOrReadOnly
from ..serializers import AnswerSerializer, AnswerListSerializer, AnswerDetailSerializer

User = get_user_model()


class AnswerViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return AnswerListSerializer
        elif self.action == 'retrieve':
            return AnswerDetailSerializer

        return AnswerSerializer

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
