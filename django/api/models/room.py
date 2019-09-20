from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=32, blank=False)
    host = models.ForeignKey(
        User,
        related_name='host',
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        User,
        related_name='users',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Room { self.pk }'

    def get_all_users(self):
        return [self.host, *self.users.all()]
