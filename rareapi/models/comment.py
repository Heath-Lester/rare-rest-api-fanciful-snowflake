from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    author= models.OneToOneField(User, on_delete=models.CASCADE)
    subject= models.CharField(max_length=25)
    comment= models.CharField(max_length=250)
    deleted= models.BooleanField()