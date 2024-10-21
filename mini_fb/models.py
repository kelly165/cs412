from django.db import models
from django.utils import timezone
from django.urls import reverse



class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_image_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        # Returns all StatusMessage objects related to this profile, ordered by timestamp (newest first)
        return self.status_messages.all().order_by('-timestamp')
    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.pk)])
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically set timestamp
    message = models.TextField()  # Text of the status message
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='status_messages')
    
    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name}: {self.message[:30]}"  # First 30 characters of the message
    def get_images(self):
        # Returns all Image objects related to this status message
        return self.images.all()
class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')  # Make sure media settings are configured
    timestamp = models.DateTimeField(auto_now_add=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.status_message} uploaded at {self.timestamp}"