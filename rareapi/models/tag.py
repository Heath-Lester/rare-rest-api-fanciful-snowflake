from django.db import models
from rest_framework.authtoken.models import Token

class Tag(models.Model):
    author = models.ForeignKey(Token, on_delete=models.CASCADE)
    label = models.CharField(max_length=25)