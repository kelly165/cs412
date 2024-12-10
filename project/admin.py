from django.contrib import admin
from .models import Occasion, ClothingItem, Profile, Outfit, OutfitItem

# registering models with the admin site to manage them through the django admin interface

admin.site.register(Occasion)
admin.site.register(ClothingItem)
admin.site.register(Profile)
admin.site.register(Outfit)
admin.site.register(OutfitItem)
