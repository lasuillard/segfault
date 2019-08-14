from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from ..models import ChatRoom, Chat
from ..serializers import ChatRoomSerializer, ChatSerializer
from ..permissions import IsOwnerOrReadOnly

User = get_user_model()


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Chat.objects.all()
        room = self.request.query_params.get('room', default=None)
        if room is not None:
            queryset = queryset.filter(room__pk=room)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
