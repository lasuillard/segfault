from django.contrib.auth.models import User
from rest_framework import viewsets, authentication, permissions
from .serializers import UserSerializer, AvatarSerializer
from .models import Avatar


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AvatarViewSet(viewsets.ModelViewSet):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
