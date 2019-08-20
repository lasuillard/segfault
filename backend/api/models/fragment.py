from django.db import models
from django.contrib import auth, admin
from django.contrib.postgres.fields import ArrayField
from .comment import Commentable
from .vote import Votable


class Fragment(Commentable, Votable):
    user = models.ForeignKey(
        auth.get_user_model(),
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
    )
    is_closed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Fragment { self.pk } (by { self.user })'

    def get_answer_count(self):
        return self.answer_set.count()


class ArrayFieldListFilter(admin.SimpleListFilter):
    title = 'Tags'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        tags = Fragment.objects.values_list('tags', flat=True)
        tags = [(t, t) for sublist in tags for t in sublist if t]
        tags = sorted(set(tags))
        return tags

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(tags__contains=[lookup_value])

        return queryset


@admin.register(Fragment)
class FragmentAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'user', 'title_length', 'content_length',
        'tag_count', 'is_closed', 'get_average_rating', 'date_created', 'date_modified'
    ]
    list_display_links = ['pk']
    list_filter = [ArrayFieldListFilter, 'is_closed']
    search_fields = ['tags']

    def title_length(self, obj):
        return f'{ len(obj.title) } Chars'
    title_length.short_description = 'Title'

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'

    def tag_count(self, obj):
        return f'{ len(obj.tags) } Tags'
    tag_count.short_description = 'Tags'
