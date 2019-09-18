from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from api.models import Vote
from ..serializers import VoteSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class VoteViewSet(ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [IsOwnerOrReadOnly]

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
