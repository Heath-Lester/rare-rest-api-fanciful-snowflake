from django.db import models
from rest_framework.authtoken.models import Token

class Comment(models.Model):
    author= models.ForeignKey(Token, on_delete=models.CASCADE)
    subject= models.CharField(max_length=25)
    comment= models.CharField(max_length=250)
    deleted= models.BooleanField()