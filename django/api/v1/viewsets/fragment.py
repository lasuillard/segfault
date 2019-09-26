from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from core.models import Fragment
from ..serializers import FragmentSerializer, FragmentDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class FragmentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return FragmentSerializer

        return FragmentDetailSerializer

    def get_queryset(self):
        queryset = Fragment.objects.all().order_by('-date_created')
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
