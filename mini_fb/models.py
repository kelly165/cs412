from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)  # Associate Profile with User
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
    
    def get_friends(self):
        from .models import Friend  # Avoid circular imports

        # Geet friends where this profile is profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        # Combine and fetch profile instances avoiding duplicates
        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        return Profile.objects.filter(id__in=friend_ids)
    def add_friend(self, other):
    # Ensure the other Profile isn't self to avoid self-friending
        if self == other:
            return

        # Check for existing Friend relationships (either direction)
        if not Friend.objects.filter(
            profile1=self, profile2=other
        ).exists() and not Friend.objects.filter(
            profile1=other, profile2=self
        ).exists():
            # Create and save a new Friend instance if no relationship exists
            Friend.objects.create(profile1=self, profile2=other)
    def get_friend_suggestions(self):
        # Get all profiles except the current one
        all_profiles = Profile.objects.exclude(pk=self.pk)
        
        # Get friends of the current profile
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        
        # Gettting the ids of the friends
        friend_ids = [friend.profile1.pk if friend.profile1 != self else friend.profile2.pk for friend in friends]
        
        # Filter out friends from allprofiles
        friend_suggestions = all_profiles.exclude(pk__in=friend_ids)
        
        return friend_suggestions
    
    def get_news_feed(self):
        # Start with the user's own status messages
        own_messages = self.get_status_messages()

        # Get friends
        friends = self.get_friends()

        # Get friends' status messages
        friends_messages = StatusMessage.objects.filter(profile__in=friends)

        # Combine the two QuerySets and order by creation date (most recent first)
        all_messages = own_messages | friends_messages
        return all_messages.order_by('-timestamp')  # Assuming `created_at` is the field for message creation time


class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"

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