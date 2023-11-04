from django.contrib import admin
from .models import Email, User  # Import the Email model from your models.py file

# Register your models here.
admin.site.register(User)
admin.site.register(Email)
