from django.db import models

from user.models import User


class Board(models.Model):
    BOARD_TYPES = (
        ("G", "General"),
        ("M", "Materials"),
    )

    type = models.CharField(max_length=1, choices=BOARD_TYPES)


class Post(models.Model):
    writer = models.ForeignKey(
        User, related_name="posts", null=True, on_delete=models.SET_NULL
    )
    board = models.ForeignKey(
        Board, related_name="posts", null=True, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
