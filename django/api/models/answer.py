from django.db import models
from django.contrib import auth, admin
from .comment import Commentable
from .vote import Votable
from .fragment import Fragment


class Answer(Commentable, Votable):
    user = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        Fragment,
        on_delete=models.CASCADE,
    )
    content = models.TextField(blank=False)
    is_selected = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Answer { self.pk } ({ self.target })'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'target', 'content_length', 'is_selected', 'date_created', 'date_modified']
    list_display_links = ['pk']
    list_filter = ['is_selected']
    search_fields = ['user__username']

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'
