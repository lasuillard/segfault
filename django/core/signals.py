import logging
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver
from core.models import Avatar

User = get_user_model()

logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=User)
def auto_create_avatar_on_user_created(sender, instance, created, **kwargs):
    """
    Create avatar instance along with creation of user instance
    """
    if not instance.pk:
        return False

    if created:
        Avatar.objects.create(user=instance, display_name=instance.username)
        logger.debug('Created avatar instance for user in response to User.post_save signal')
