from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=75)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} - {self.friend.username} ({self.status})"