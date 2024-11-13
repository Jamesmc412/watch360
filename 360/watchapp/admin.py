from django.contrib import admin

from .models import Profile, YouTubeData, OnlineStatus, Message


# Register your models here.
admin.site.register(YouTubeData)
admin.site.register(Profile)
admin.site.register(OnlineStatus)

# Register your models here.
# This allows the Admin to view actual info.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')