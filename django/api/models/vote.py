from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# interface class for resources that can be voted
class Votable(models.Model):
    votable_id = models.AutoField(primary_key=True)

    def get_child_object(self):
        for cls in Votable.__subclasses__():
            child = cls.__name__.lower()
            if hasattr(self, child):
                return getattr(self, child)

        return None
    get_child_object.short_description = 'Related child'

    def get_vote_count(self):
        return self.vote_set.count()

    def get_average_rating(self):
        return float(self.vote_set.aggregate(models.Avg('rating'))['rating__avg'] or 0.0)
    get_average_rating.short_description = 'Rating'

    def __str__(self):
        return f'{ self.get_child_object() }'


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Good'),
        (-1, 'Bad')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        Votable,
        on_delete=models.CASCADE,
    )
    rating = models.DecimalField(max_digits=1, decimal_places=0, choices=VOTE_CHOICES)

    def __str__(self):
        return f'Vote { self.pk } ... { self.target }'
