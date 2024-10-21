from django.contrib import admin
from .models import Profile, StatusMessage, Image

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'email')

admin.site.register(StatusMessage)
admin.site.register(Image)
