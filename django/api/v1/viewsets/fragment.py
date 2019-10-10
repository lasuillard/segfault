from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Fragment
from api.permissions import IsAdminUser, IsOwner
from ..serializers import FragmentSerializer, FragmentListSerializer, FragmentDetailSerializer

User = get_user_model()


class FragmentViewSet(ModelViewSet):
    """
    API for fragment resources

    avatar : exact match for avatar primary key or case-insensitive inclusion for display name
    title  : case-insensitive partial match for content
    content: case-insensitive partial match for content
    status : exact match for status
    tags   : partial inclusion for tags with exact match, separated with comma(,)
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return FragmentListSerializer
        elif self.action == 'retrieve':
            return FragmentDetailSerializer
        # for data modifications
        return FragmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny, ]
        elif self.action == 'create':
            permissions = [IsAuthenticated | IsAdminUser, ]
        else:
            permissions = [IsOwner | IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Fragment.objects.all().order_by('-date_created')
        query_params = self.request.query_params

        # avatar, exact match for primary key or case-insensitive partial match for display name
        avatar = query_params.get('avatar')
        if avatar:
            try:
                avatar = int(avatar)
                queryset = queryset.filter(user__avatar__pk=avatar)
            except ValueError:
                queryset = queryset.filter(user__avatar__display_name__icontains=avatar)

        # title, case in-sensitive partial match for content
        title = query_params.get('title')
        queryset = queryset.filter(title__icontains=title) if title else queryset

        # content, case in-sensitive partial match for content
        content = query_params.get('content')
        queryset = queryset.filter(content__icontains=content) if content else queryset

        # status, exact match for status
        status = query_params.get('status')
        queryset = queryset.filter(status=status) if status else queryset

        # tags, partial inclusion for tags
        tags = query_params.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
