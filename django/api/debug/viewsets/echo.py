import json
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import FCMDeviceSerializer

User = get_user_model()


class EchoViewSet(ViewSet):
    """
    An echo api view for testing ws/fcm notification services
    """
    name = 'Echo'

    def get_permissions(self):
        if settings.DEBUG:
            permissions = [IsAuthenticated, ]
        else:
            return False

        return [permission() for permission in permissions]

    def list(self, request):
        user = request.user
        channel_group = user.avatar.get_channel_group()
        devices = FCMDevice.objects.filter(user=user)
        return Response({
            'current_user': f'{user.username}/{user.email}',
            'channel_group': channel_group,
            'devices': FCMDeviceSerializer(devices, many=True).data
        })

    @action(detail=False, methods=['post'], url_path='ws-notification', url_name='ws-notification')
    def ws_notification_echo(self, request):
        """
        Send echo to notification websocket of current user.
        """
        user = request.user
        data = json.dumps(request.data)
        channel_layer = get_channel_layer()
        try:
            channel_group = user.avatar.get_channel_group()
            async_to_sync(channel_layer.group_send)(
                channel_group,
                {
                    'type': 'notification.send',
                    'message': {
                        'title': 'SegFault WebSocket Notification Echo',
                        'body': data
                    }
                }
            )
            return Response(data={'echo': data}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response(
                data={'message': "User has no avatar; server malfunctioning."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='fcm', url_name='fcm')
    def fcm_echo(self, request):
        """
        Send echo to registered FCM devices of current user.
        """
        user = request.user
        data = json.dumps(request.data)
        try:
            device = FCMDevice.objects.filter(user=user)
            device.send_message(
                title='SegFault FCM Echo',
                body=data
            )
            return Response(data={'echo': data}, status=status.HTTP_200_OK)
        except FCMDevice.DoesNotExist:
            return Response(
                data={'message': "There's no device for user."},
                status=status.HTTP_400_BAD_REQUEST)
