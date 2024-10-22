from django.db import models
from django.contrib.auth.models import User

class YouTubeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()
    video_title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)  # Optional: To track when videos were added

    def __str__(self):
        return self.video_title
