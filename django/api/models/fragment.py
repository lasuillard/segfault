from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField
from .comment import Commentable
from .vote import Votable

User = get_user_model()


class Fragment(Commentable, Votable):
    STATUS = Choices('OPEN', 'CLOSED')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=256)
    content = models.TextField()
    tags = ArrayField(
        models.CharField(  # consider using SlugField instead
            max_length=16,
            blank=True,
        ),
        # size=16,
        default=list,
        blank=True
    )
    status = StatusField(choices=STATUS, default=STATUS.OPEN)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_closed = MonitorField(monitor='status', when=[STATUS.CLOSED], default=None, null=True, blank=True, editable=False)

    def __str__(self):
        return f'Fragment { self.pk }'

    def get_answer_count(self):
        return self.answer_set.count()
