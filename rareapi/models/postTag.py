from django.db import models

class PostTag(models.Model):
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    tag = models.ForeignKey("tag", on_delete=models.CASCADE)