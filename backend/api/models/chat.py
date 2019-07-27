from django.db import models
from django.contrib import auth, admin

User = auth.get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=32, blank=False)
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        User,
        related_name='users',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chat room { self.pk }'

    def get_all_attendants(self):
        # merge queryset and return it
        attendants = list([user for user in self.users.all()])
        attendants.append(self.user)
        return attendants


class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
    )
    content = models.TextField(max_length=1024, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chat { self.pk } ({ self.room })'


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'user_count', 'date_created', 'date_modified']
    list_display_links = ['pk']
    search_fields = ['user__username', 'name']

    def user_count(self, obj):
        return f'{ obj.users.all().count() } Users'
    user_count.short_description = 'User'


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'room', 'content_length', 'date_created', 'date_modified']
    list_display_links = ['pk']
    list_filter = ['user', 'room']
    search_fields = ['user__username', 'room__name']

    def content_length(self, obj):
        return f'{ len(obj.content) } Chars'
    content_length.short_description = 'Content'
