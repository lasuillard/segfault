from django.db import models
from django.contrib.auth import get_user_model
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField
from .comment import Commentable
from .vote import Votable
from .tag import Tag

User = get_user_model()


class Fragment(Commentable, Votable):
    STATUS = Choices('OPEN', 'CLOSED')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=256)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    status = StatusField(choices=STATUS, default=STATUS.OPEN)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_closed = MonitorField(
        monitor='status', when=[STATUS.CLOSED], default=None, null=True, blank=True, editable=False
    )

    def __str__(self):
        return f"{ self.pk } { self.title[:10] if len(self.title) > 10 else self.title }"

    def get_answer_count(self):
        if not hasattr(self, 'answer_set'):
            raise AttributeError('answer_set does not exists. please be make sure that model Answer has target field.')

        return self.answer_set.count()
