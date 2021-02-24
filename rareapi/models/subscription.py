from django.db import models
from rest_framework.authtoken.models import Token


class Subscription(models.Model):
    follower = models.ForeignKey(Token, on_delete=models.CASCADE, related_name = "subscriber")
    author = models.ForeignKey(Token, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    ended_on = models.DateTimeField(auto_now=False, auto_now_add=False)