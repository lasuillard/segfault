import os
import random
from uuid import uuid4

from django.db import models
from django.dispatch import receiver
from django.contrib import auth, admin
from django.contrib.postgres.fields import JSONField

User = auth.get_user_model()
DEFAULT_PROFILE_IMAGES = ['avatar/default.png']


def get_image_uuid4(instance, filename):
    return os.path.join('avatar', f"{ uuid4() }.{ filename.split('.')[-1] }")


class Avatar(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    profile_image = models.ImageField(upload_to=get_image_uuid4, default=random.choice(DEFAULT_PROFILE_IMAGES))
    display_name = models.CharField(max_length=32)
    introduce_message = models.TextField(null=True, blank=True)
    user_data = JSONField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'user'

    def __str__(self):
        return f'Avatar { self.pk } (for { self.user.username })'

    def save(self, *args, **kwargs):
        # TODO: check profile image, and resize it

        # give default display name as user's account name
        if self.display_name is None or len(self.display_name) == 0:
            self.display_name = self.user.username

        super(Avatar, self).save(*args, **kwargs)


@receiver(models.signals.post_save, sender=User)
def auto_create_avatar_on_user_created(sender, instance, created, **kwargs):
    """
        create avatar instance along with creation of user instance
    """
    if not instance.pk:
        return False

    if created:
        Avatar.objects.create(user=instance, display_name=instance.username)


@receiver(models.signals.pre_save, sender=Avatar)
def auto_delete_profile_image_on_change(sender, instance, **kwargs):
    """
        delete image file stored in filesystem
        when corresponding one is updated with new one
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).profile_image
    except sender.DoesNotExist:
        return False

    if old_file.name in DEFAULT_PROFILE_IMAGES:
        return False

    new_file = instance.profile_image
    if not old_file == new_file:
        if os.path.exists(old_file.path):
            old_file.delete(save=False)
        else:
            pass


@receiver(models.signals.post_delete, sender=Avatar)
def auto_delete_profile_image_on_delete(sender, instance, **kwargs):
    """
        delete image file from filesystem
    """
    file = instance.profile_image
    if os.path.exists(file.path) and file.name not in DEFAULT_PROFILE_IMAGES:
        file.delete(save=False)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'profile_image', 'display_name', 'date_modified']
    list_display_links = ['pk']
    search_fields = ['pk', 'user__username', 'display_name']
