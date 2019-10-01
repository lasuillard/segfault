from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import Fragment
from api.permissions import IsAdminUser, IsOwner
from ..serializers import FragmentSerializer, FragmentListSerializer, FragmentDetailSerializer

User = get_user_model()


class FragmentViewSet(ModelViewSet):

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

        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
