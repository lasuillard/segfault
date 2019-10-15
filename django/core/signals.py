import logging
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver
from core.models import Avatar, Fragment, Answer, Notification

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


@receiver(signals.post_save, sender=Answer)
def send_fcm_push_to_fragment_poster_on_answer_post(sender, instance, created, **kwrags):
    """
    Make and send FCM push to fragment owner when answer is created for it
    """
    if not instance.pk:
        return False

    if created:
        fragment = instance.target
        if instance.user == fragment.user:
            return

        notification = Notification.objects.create(
            title='SegFault',
            body="There's new answer for your fragment",
            extra_data={'answer_id': instance.pk}
        )
        notification.users.set([fragment.user, ])
        notification.send(fcm_push=True)
