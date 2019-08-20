from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from ..models import Fragment
from ..serializers import FragmentSerializer, FragmentDetailSerializer
from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class FragmentViewSet(ModelViewSet):
    serializer_class = FragmentSerializer
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

