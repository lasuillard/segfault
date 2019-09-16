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

app_name = 'v1'

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'avatar', AvatarViewSet, basename='avatar')
router.register(r'fragment', FragmentViewSet, basename='fragment')
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'vote', VoteViewSet, basename='vote')
router.register(r'chatroom', ChatRoomViewSet, basename='chatroom')
router.register(r'chat', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls))
]
