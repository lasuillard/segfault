from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from ..models import Vote
from ..serializers import VoteSerializer
from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class VoteViewSet(ModelViewSet):
    serializer_class = VoteSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Vote.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)