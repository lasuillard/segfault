from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    UserViewSet,
    AvatarViewSet,
    FragmentViewSet,
    AnswerViewSet,
    CommentViewSet,
    VoteViewSet,
    ChatRoomViewSet,
    ChatViewSet,
)

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'avatar', AvatarViewSet)
router.register(r'fragment', FragmentViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'vote', VoteViewSet)
router.register(r'chatroom', ChatRoomViewSet)
router.register(r'chat', ChatViewSet)

urlpatterns = [
    path('', include(router.urls))
]
