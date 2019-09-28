from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from core.models import Fragment
from api.permissions import IsAdminUser, IsOwnerOrReadOnly
from ..serializers import FragmentSerializer, FragmentListSerializer, FragmentDetailSerializer

User = get_user_model()


class FragmentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return FragmentListSerializer
        elif self.action == 'retrieve':
            return FragmentDetailSerializer

        return FragmentSerializer

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
