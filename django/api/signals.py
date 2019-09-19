import os
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver
from .models import Avatar, AVATAR_DEFAULT_IMAGE

User = get_user_model()


@receiver(signals.post_save, sender=User)
def auto_create_avatar_on_user_created(sender, instance, created, **kwargs):
    """
        create avatar instance along with creation of user instance
    """
    if not instance.pk:
        return False

    if created:
        Avatar.objects.create(user=instance, display_name=instance.username)


@receiver(signals.pre_save, sender=Avatar)
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

    if old_file.name == AVATAR_DEFAULT_IMAGE:
        return False

    new_file = instance.profile_image
    if not old_file == new_file:
        if os.path.exists(old_file.path):
            old_file.delete(save=False)
        else:
            pass


@receiver(signals.post_delete, sender=Avatar)
def auto_delete_profile_image_on_delete(sender, instance, **kwargs):
    """
        delete image file from filesystem
    """
    file = instance.profile_image
    if os.path.exists(file.path) and file.name != AVATAR_DEFAULT_IMAGE:
        file.delete(save=False)
