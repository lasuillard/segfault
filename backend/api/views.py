from rest_framework import viewsets
from .serializers import AvatarSerializer
from .models import Avatar


class AvatarViewSet(viewsets.ModelViewSet):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()
