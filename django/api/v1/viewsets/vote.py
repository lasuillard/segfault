from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from core.models import Vote
from api.permissions import IsAdminUser, IsOwnerOrReadOnly
from ..serializers import VoteSerializer, VoteListSerializer, VoteDetailSerializer

User = get_user_model()


class VoteViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return VoteListSerializer
        elif self.action == 'retrieve':
            return VoteDetailSerializer

        return VoteSerializer

    def get_queryset(self):
        queryset = Vote.objects.all()
        user = self.request.query_params.get('user', default=None)
        target = self.request.query_params.get('target', default=None)

        if user is not None:
            queryset = queryset.filter(user__pk=user)

        if target is not None:
            queryset = queryset.filter(target__pk=target)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
