from django.db import models
from django.contrib.auth import get_user_model
from .room import Room

User = get_user_model()


class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=1024, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{ self.pk } for Room { self.room })'
