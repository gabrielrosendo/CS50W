from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image_url = models.URLField()
    current_price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

