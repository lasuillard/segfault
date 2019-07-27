from django.db import models
from django.contrib import auth, admin

VOTE_CHOICES = (
    (-2, 'Very impractical'),
    (-1, 'Impractical'),
    (0, 'Hmm'),
    (1, 'Useful'),
    (2, 'Very useful'),
)


# interface class for resources that can be voted
class Votable(models.Model):
    votable_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{ self.get_child_object() }'

    def get_child_object(self):
        for cls in Votable.__subclasses__():
            child = cls.__name__.lower()
            if hasattr(self, child):
                return getattr(self, child)

        return None
    get_child_object.short_description = 'Related child'

    def get_average_rating(self):
        return float(self.vote_set.aggregate(models.Avg('rating'))['rating__avg'])
    get_average_rating.short_description = 'Rating'


class Vote(models.Model):
    user = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        Votable,
        on_delete=models.CASCADE,
    )
    rating = models.DecimalField(max_digits=1, decimal_places=0, choices=VOTE_CHOICES)

    def __str__(self):
        return f'Vote { self.pk } ({ self.target })'


@admin.register(Votable)
class VotableAdmin(admin.ModelAdmin):
    list_display = ['pk', 'get_child_object']
    list_display_links = ['pk']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'target', 'rating']
    list_filter = ['rating']
    search_fields = ['user__username', 'target__id']
