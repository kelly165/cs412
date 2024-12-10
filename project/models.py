from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


# occasion model to define different types of occasions
class Occasion(models.Model):
    OCCASION_CHOICES = [
        ('Casual', 'Casual'),
        ('Formal', 'Formal'),
        ('Business', 'Business'),
        ('Party', 'Party'),
        ('Outdoor', 'Outdoor'),
        ('Sports', 'Sports'),
    ]
    name = models.CharField(max_length=20, choices=OCCASION_CHOICES, unique=True)

    def __str__(self):
        return self.name

# clothing item model to store attributes of clothing items such as name, category, color, etc.
class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
        ('Shoes', 'Shoes'),
        ('Accessory', 'Accessory'),
    ]
    SEASON_CHOICES = [
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=10)
    season = MultiSelectField(choices=SEASON_CHOICES)
    image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)  # optional image for clothing item
    occasions = models.ManyToManyField(Occasion)  # many-to-many relationship with occasions
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clothing_items')  # links to a user

    def __str__(self):
        return self.name

# profile model to store a user's profile, including their profile picture
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')  # one-to-one relationship with user
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # optional profile picture

    def __str__(self):
        return self.user.username

# outfit model to define outfits with a name, description, and a user
class Outfit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # links to a user

    def __str__(self):
        return self.name

# outfit item model to link clothing items to outfits
class OutfitItem(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)  # links to an outfit
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)  # links to a clothing item

    def __str__(self):
        return f"{self.outfit.name} - {self.clothing_item.name}"  # string representation of the outfit and clothing item