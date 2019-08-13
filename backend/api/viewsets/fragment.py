from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from ..models import Fragment
from ..serializers import FragmentSerializer
from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class FragmentViewSet(ModelViewSet):
    serializer_class = FragmentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Fragment.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

