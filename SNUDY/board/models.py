from django.db import models

from user.models import User


class Board(models.Model):
    BOARD_TYPES = (
        ("G", "General"),
        ("M", "Materials"),
    )

    type = models.CharField(max_length=1, choices=BOARD_TYPES)


class Post(models.Model):
    writer = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    commenter = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", related_name="replies", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
