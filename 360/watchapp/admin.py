from django.contrib import admin

from .models import Profile
from .models import YouTubeData

admin.site.register(YouTubeData)


# Register your models here.

admin.site.register(Profile)