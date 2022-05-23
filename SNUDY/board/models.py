from django.db import models

from user.models import User


class Board(models.Model):
    BOARD_TYPES = (
        ("G", "General"),
        ("M", "Materials"),
    )

    type = models.CharField(max_length=1, choices=BOARD_TYPES)


class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True
    )
    content = models.CharField(max_length=255)
    is_anonymous = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
