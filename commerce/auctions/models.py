from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('auctions.Listing', blank=True,default=None)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image_url = models.URLField()
    current_price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

class Comment(models.Model):
    text = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField()



