from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from ..models import Comment
from ..serializers import CommentSerializer
from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        user = self.request.query_params.get('user', default=None)
        target = self.request.query_params.get('target', default=None)

        if user is not None:
            queryset = queryset.filter(user__pk=user)

        if target is not None:
            queryset = queryset.filter(target__pk=target)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
