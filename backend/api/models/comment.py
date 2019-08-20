from django.db import models
from django.contrib import auth, admin


# interface class for resources that can be commented
class Commentable(models.Model):
    commentable_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{ self.get_child_object() }'

    def get_child_object(self):
        for cls in Commentable.__subclasses__():
            child = cls.__name__.lower()
            if hasattr(self, child):
                return getattr(self, child)

        return None
    get_child_object.short_description = 'Related child'

    def get_comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        Commentable,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment { self.pk } ({ self.target })'


@admin.register(Commentable)
class CommentableAdmin(admin.ModelAdmin):
    list_display = ['pk', 'get_child_object']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'parent', 'user', 'target', 'content_length', 'date_created', 'date_modified']

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'
