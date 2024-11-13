from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class YouTubeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.URLField()
    video_title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()  # Duration in seconds

    def __str__(self):
        return self.video_title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default.jpg')
    bio = models.TextField(max_length=500, blank=True, null=True)  # Add this line for bio

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path) 
            
class OnlineStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    video_title = models.OneToOneField(YouTubeData, on_delete=models.CASCADE, default=1)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Online Status'