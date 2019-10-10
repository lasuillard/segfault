from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    EchoViewSet,
)

app_name = 'debug'

router = DefaultRouter()
router.register(r'echo', EchoViewSet, basename='echo')

urlpatterns = [
    path('', include(router.urls))
]
