from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Changed: Removed university_id, made email unique and required
    email = models.EmailField(unique=True)
    is_online = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Use email for login instead of username (optional but common for modern apps)
    # USERNAME_FIELD = 'email' 
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class ChatSession(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_user2', null=True)
    # Check these names below!
    is_active = models.BooleanField(default=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

class CampusNetwork(models.Model):
    name = models.CharField(max_length=100) # e.g., "VU Main Campus"
    public_ip = models.GenericIPAddressField() # The external IP
    
    def __str__(self):
        return self.name