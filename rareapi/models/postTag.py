from django.db import models
from rest_framework.authtoken.models import Token

class PostTag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="tagging")
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tagging")