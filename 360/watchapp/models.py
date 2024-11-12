from django.db import models
from django.contrib.auth.models import User

class YouTubeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.URLField()
    video_title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()  # Duration in seconds
    scheduled_deletion_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.video_title


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, default=1)  # Set a default user ID
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} at {self.timestamp}: {self.content}"
    
    