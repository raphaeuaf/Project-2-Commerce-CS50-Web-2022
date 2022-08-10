from django.contrib.auth.models import AbstractUser
from django.db import models
#from more_itertools import value_chain


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction", blank=True, related_name="user")


class Category(models.Model):
    category = models.CharField(max_length=64)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.category


class Auction(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    start_bid = models.FloatField()
    thereis_bid = models.BooleanField(default=False)
    current_bid = models.FloatField(default=0)
    image_url = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, blank=True, related_name="auctions")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    date_published = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    amount = models.FloatField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment")
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)