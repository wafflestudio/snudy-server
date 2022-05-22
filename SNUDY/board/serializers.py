from requests import request
from rest_framework import serializers

from django.shortcuts import get_object_or_404

from board.models import Post, Board


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    is_anonymous = serializers.BooleanField(required=False)

    def validate(self, data):
        user = self.context.get("user")
        if user is None:
            raise serializers.ValidationError()

        board_id = self.context.get("board_id")
        board = get_object_or_404(Board, pk=board_id)
        return data

    def create(self, validated_data):
        user = self.context["user"]
        board_id = self.context["board_id"]
        board = get_object_or_404(Board, pk=board_id)

        post = Post.objects.create(writer=user, board=board, **validated_data)
        return post
