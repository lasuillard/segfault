from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import (
    Avatar,
    Fragment,
    Answer,
    Comment,
    Vote,
    ChatRoom,
    Chat,
)
from .serializers import (
    UserSerializer,
    AvatarSerializer,
    FragmentSerializer,
    AnswerSerializer,
    CommentSerializer,
    VoteSerializer,
    ChatRoomSerializer,
    ChatSerializer,
)
from .permissions import (
    ReadOnly,
    IsOwnerOrReadOnly,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [ReadOnly]

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', default=None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)

        return queryset


class AvatarViewSet(ModelViewSet):
    serializer_class = AvatarSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Avatar.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(Q(user__pk=user) | Q(user__username=user))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Answer.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteViewSet(ModelViewSet):
    serializer_class = VoteSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Vote.objects.all()
        user = self.request.query_params.get('user', default=None)
        if user is not None:
            queryset = queryset.filter(user__pk=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
