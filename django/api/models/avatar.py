import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


def get_image_uuid4(instance, filename):
    return os.path.join('avatar', f"{ uuid4() }.{ filename.split('.')[-1] }")


class Avatar(models.Model):
    AVATAR_DEFAULT_IMAGE = 'avatar_default_image.png'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=get_image_uuid4, default=AVATAR_DEFAULT_IMAGE)
    display_name = models.CharField(max_length=32)
    introduce_message = models.CharField(null=True, blank=True, max_length=128)
    extra_data = JSONField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'user'

    def __str__(self):
        return f'Avatar { self.pk } ... User { self.user }'

    def save(self, *args, **kwargs):
        # give default display name as user's account name
        if self.display_name is None or len(self.display_name) == 0:
            self.display_name = self.user.username

        super(Avatar, self).save(*args, **kwargs)
