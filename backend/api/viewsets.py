from django.contrib.auth import get_user_model
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

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class AvatarViewSet(ModelViewSet):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FragmentViewSet(ModelViewSet):
    serializer_class = FragmentSerializer
    queryset = Fragment.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class VoteViewSet(ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class ChatRoomViewSet(ModelViewSet):
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]
