from django.db import models
from django.contrib.auth import get_user_model
from .comment import Commentable
from .vote import Votable
from .fragment import Fragment

User = get_user_model()


class Answer(Commentable, Votable, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    target = models.ForeignKey(Fragment, on_delete=models.CASCADE, )
    content = models.CharField(
        blank=False,
        max_length=2048,
        help_text='Answer for a fragment, maximum length of 2048.',
    )
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{ self.pk } for Fragment { self.target }'
