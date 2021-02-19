from django.db import models
from rest_framework.authtoken.models import Token

class Post(models.Model):
    author= models.ForeignKey(Token, on_delete=models.CASCADE)
    category= models.ForeignKey("category", on_delete=models.CASCADE)
    title= models.CharField(max_length=15)
    content= models.CharField(max_length=250)
    publication_date= models.DateTimeField(auto_now=False, auto_now_add=False)
    image_url= models.CharField(max_length=50)
    approved= models.BooleanField()
    deleted= models.BooleanField()