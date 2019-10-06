from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from core.models import Tag
from ..serializers import TagSerializer, TagListSerializer, TagDetailSerializer

User = get_user_model()


class TagViewSet(ModelViewSet):
    """
    API for tag resources

    name       : case-insensitive partial match for name
    is_official: boolean for is_official, true or false, display all when not specified.
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return TagListSerializer
        elif self.action == 'retrieve':
            return TagDetailSerializer

        return TagSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permissions = [AllowAny, ]
        else:
            permissions = [IsAdminUser, ]

        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Tag.objects.order_by('name')
        query_params = self.request.query_params

        # name, case-insensitive partial match for name
        name = query_params.get('name')
        queryset = queryset.filter(name__icontains=name) if name else queryset

        # is_official, boolean for is_official
        is_official = query_params.get('is_official')
        is_official = True if is_official == 'true' else False if is_official == 'false' else None
        if is_official is not None:
            queryset = queryset.filter(is_official=is_official)

        return queryset
