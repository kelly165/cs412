from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


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
    image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)
    occasions = models.ManyToManyField(Occasion)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clothing_items')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Outfit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class OutfitItem(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.outfit.name} - {self.clothing_item.name}"

