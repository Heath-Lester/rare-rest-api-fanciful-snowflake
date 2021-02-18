from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author_id: models.OneToOneField(User, on_delete=models.CASCADE)
    category_id: models.ForeignKey("category", on_delete=models.CASCADE)
    title: models.CharField(max_length=15)
    content: models.CharField(max_length=250)
    post_time: models.DateTimeField(auto_now=False, auto_now_add=False)
    image_url: models.CharField(max_length=50)
    approved: models.BooleanField()
    deleted: models.BooleanField()