from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    user = models.ForeignKey(
        User,
        related_name='host',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=32, blank=False)
    _room_channel_group = models.UUIDField(default=uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{ self.pk } { self.name[:10] if len(self.name) > 10 else self.name }"

    def get_channel_group(self):
        return str(self._room_channel_group)
