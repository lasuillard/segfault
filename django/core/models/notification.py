from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

User = get_user_model()


class Notification(models.Model):
    """
    Note: creating instance of notification model won't send it to user expected to receive.
    """
    DEBUG = 0
    INFO = 1
    WARNING = 2
    CRITICAL = 3
    NOTIFICATION_LEVELS = [
        (INFO, 'INFO'),
        (WARNING, 'WARNING'),
        (CRITICAL, 'CRITICAL'),
    ]

    # consider: StatusField with date_sent

    users = models.ManyToManyField(User)
    level = models.CharField(max_length=16, choices=NOTIFICATION_LEVELS)
    message = models.CharField(max_length=256)
    extra_data = JSONField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return f'Notification { self.pk }'
