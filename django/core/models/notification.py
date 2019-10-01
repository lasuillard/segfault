from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from channels import layers
from fcm_django.models import FCMDevice

User = get_user_model()


class Notification(models.Model):
    """
    Note: creating instance of notification model won't send it to user expected to receive.
    """

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
        # mark notification as read, and won't show next time.
        if self.users.filter(pk=user.pk).exists():
            self._users_read.add(user)
            self.users.remove(user)

    async def send(self):
        channel_layer = layers.get_channel_layer()
        for user in self.users.all():
            if not hasattr(user, 'avatar'):
                raise AttributeError(f'user has no avatar: {user}')

            # send websocket notification
            channel_group = user.avatar.get_channel_group()
            await channel_layer.group_send(
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
            # send FCM push notification
            try:
                device = FCMDevice.objects.get(user=user)
                device.send_message(
                    title=self.title,
                    body=self.body,
                    data=self.extra_data,
                    # TODO: more FCM arguments, such as sound and click actions...
                )
            except FCMDevice.DoesNotExist:
                pass
