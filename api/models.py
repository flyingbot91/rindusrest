"""
API models.
"""
from django.db import models


class Post(models.Model):
    """Post."""

    body = models.TextField()
    title = models.CharField(max_length=200)
    user_id = models.PositiveIntegerField(default=99999942)

    def __str__(self):
        return f"{self.__class__.__name__} {self.pk}: {self.title}"


class Comment(models.Model):
    """Comment."""

    body = models.TextField()
    email = models.EmailField()
    name = models.CharField(max_length=200)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.__class__.__name__} {self.pk}: {self.name}"
