# blog/admin.py
from django.contrib import admin
# tell the admin we want to administer these models


from .models import *
# Register your models here.

admin.site.register(Article)