from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Vote
from api.permissions import IsAdminUser, IsOwner
from ..serializers import VoteSerializer, VoteListSerializer, VoteDetailSerializer

User = get_user_model()


class VoteViewSet(ModelViewSet):
    """
    API for vote resources

    avatar, exact match for primary key or case-insensitive partial match for display name
    target, exact match, primary key
    rating, exact match for rating
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return VoteListSerializer
        elif self.action == 'retrieve':
            return VoteDetailSerializer

        return VoteSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny, ]
        elif self.action == 'create':
            permissions = [IsAuthenticated | IsAdminUser, ]
        else:
            permissions = [IsOwner | IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Vote.objects.order_by('-date_created')
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

        # rating, exact match for rating
        rating = query_params.get('rating')
        queryset = queryset.filter(rating=rating) if rating else queryset

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

