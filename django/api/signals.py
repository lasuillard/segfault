import os
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver
from .models import Avatar

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
