from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    author_id = models.OneToOneField(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=25)