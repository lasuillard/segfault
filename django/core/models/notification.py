from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from channels import layers
from asgiref.sync import async_to_sync
from fcm_django.models import FCMDevice

User = get_user_model()


class Notification(models.Model):
    users = models.ManyToManyField(User)
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=256)
    extra_data = JSONField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    # users who marked it as read
    _users_read = models.ManyToManyField(User, related_name='_notification_set')

    def __str__(self):
        return f"{ self.pk } { self.title[:10] if len(self.title) > 10 else self.title }"

    def mark_as_read(self, user):
        """
        mark notification as read to be not shown next time
        """
        if self.users.filter(pk=user.pk).exists():
            self._users_read.add(user)
            self.users.remove(user)

    def send(self, fcm_push=False, fcm_extra_options=None):
        """
        send web socket notification to user, and FCM push notification when specified
        """
        (count_ws_sent, count_fcm_sent) = (0, 0)
        channel_layer = layers.get_channel_layer()
        for user in self.users.all():
            # send web socket notification
            channel_group = user.avatar.get_channel_group()
            async_to_sync(channel_layer.group_send)(
                channel_group,
                {
                    'type': 'notification.send',
                    'message': {
                        'title': self.title,
                        'body': self.body,
                        'data': self.extra_data
                    }
                }
            )
            count_ws_sent += 1
            # send FCM push notification
            if fcm_push:
                devices = FCMDevice.objects.filter(user=user)
                devices.send_message(
                    title=self.title,
                    body=self.body,
                    **(fcm_extra_options if fcm_extra_options else {})
                )
                count_fcm_sent += devices.count()

        return count_ws_sent, count_fcm_sent
