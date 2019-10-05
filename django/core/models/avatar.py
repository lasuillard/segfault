import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from core.utility import TimeStampedModel

User = get_user_model()


def get_image_uuid4(instance, filename):
    return os.path.join('avatar', f"{ uuid4() }.{ filename.split('.')[-1] }")


class Avatar(models.Model):
    """
    Avatar is an model for user to store data (especially public display data)
    """
    AVATAR_DEFAULT_IMAGE = 'profile.png'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=get_image_uuid4, default=AVATAR_DEFAULT_IMAGE)
    display_name = models.CharField(max_length=32)
    introduce_message = models.CharField(null=True, blank=True, max_length=128)
    extra_data = JSONField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    # for websocket
    _notification_channel_group = models.UUIDField(default=uuid4, unique=True, editable=False)

    class Meta:
        order_with_respect_to = 'user'

    def __str__(self):
        return f'{ self.pk } for User { self.user }'

    def save(self, *args, **kwargs):
        # give default display name as user's account name
        if self.display_name is None or len(self.display_name) == 0:
            self.display_name = self.user.username

        # delete old profile image when changed to new one
        try:
            old_profile_image = Avatar.objects.get(pk=self.pk).profile_image  # no substitute?
            new_profile_image = self.profile_image
            if old_profile_image.name != self.AVATAR_DEFAULT_IMAGE:
                if old_profile_image != new_profile_image and os.path.exists(old_profile_image.path):
                    old_profile_image.delete(save=False)
        except Avatar.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        profile_image = self.profile_image
        if profile_image.name != Avatar.AVATAR_DEFAULT_IMAGE and os.path.exists(profile_image.path):
            profile_image.delete(save=False)

        super().delete(*args, **kwargs)

    def get_channel_group(self):
        return str(self._notification_channel_group)
