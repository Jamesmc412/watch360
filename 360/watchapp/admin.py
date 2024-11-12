from django.contrib import admin

from .models import Profile, YouTubeData, OnlineStatus

# Register your models here.

admin.site.register(Profile)
admin.site.register(YouTubeData)
admin.site.register(OnlineStatus)