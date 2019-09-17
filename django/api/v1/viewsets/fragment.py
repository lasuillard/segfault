from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from api.models import Fragment
from ..serializers import FragmentSerializer, FragmentDetailSerializer
from api.permissions import IsOwnerOrReadOnly

User = get_user_model()


class FragmentViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FragmentDetailSerializer

        return FragmentSerializer

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

