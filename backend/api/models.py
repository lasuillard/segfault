from django.db import models
from django.contrib.auth.models import User
from django.core import validators


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.FileField()
    display_name = models.CharField(max_length=32)
    introduce_message = models.TextField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Avatar of { self.user.name }'
