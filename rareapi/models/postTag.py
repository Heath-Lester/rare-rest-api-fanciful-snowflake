from django.db import models
from rest_framework.authtoken.models import Token


# Only need tagging on tag because virtual/custom property on post.py relates to tags
class PostTag(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tagging")

