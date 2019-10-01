from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'device', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path('fcm/', include(router.urls)),
]
