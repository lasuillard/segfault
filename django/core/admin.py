from django.contrib import admin
from core.models import Avatar, Fragment, Tag, Answer, Comment, Vote, Room, Chat, Notification


admin.site.empty_value_display = '(None)'


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'profile_image', 'display_name', 'date_modified']
    list_display_links = ['pk']
    search_fields = ['pk', 'user__username', 'display_name']


@admin.register(Fragment)
class FragmentAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'user', 'title_length', 'content_length',
        'tag_count', 'status', 'get_average_rating', 'date_created', 'date_modified', 'date_closed'
    ]
    list_display_links = ['pk']
    list_filter = ['status']
    search_fields = ['tags']

    def title_length(self, obj):
        return f'{ len(obj.title) } Chars'
    title_length.short_description = 'Title'

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'

    def tag_count(self, obj):
        return f'{ obj.tags.count() } Tags'
    tag_count.short_description = 'Tags'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'is_official']
    list_display_links = ['pk']
    list_filter = ['is_official']
    search_fields = ['name']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'target', 'content_repr', 'date_created', 'date_modified']
    list_display_links = ['pk']
    search_fields = ['user__username']

    def content_repr(self, obj):
        return f'{ len(obj.content) } Chars'
    content_repr.short_description = 'Content'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'target', 'parent', 'content_length', 'date_created', 'date_modified']
    search_fields = ['user__username']

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'target', 'rating']
    list_filter = ['rating']
    search_fields = ['user__username', 'target__id']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'name', 'date_created', 'date_modified']
    list_display_links = ['pk']
    search_fields = ['name']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'room', 'content_length', 'date_created', 'date_modified']
    list_display_links = ['pk']
    list_filter = ['room']
    search_fields = ['user__username', 'room__name']

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_count_related', 'title_length', 'body_length', 'date_created']
    list_display_links = ['pk']

    def user_count_related(self, obj):
        return f'{ obj.users.all().count() } Users'
    user_count_related.short_description = 'Users'

    def title_length(self, obj):
        return f'{ len(obj.message) } Chars'
    title_length.short_description = 'Title'

    def body_length(self, obj):
        return f'{ len(obj.message) } Chars'
    body_length.short_description = 'Body'
