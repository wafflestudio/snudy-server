from requests import request
from rest_framework import serializers

from django.shortcuts import get_object_or_404

from board.models import Post, Board


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
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
        user = self.context.get("user")
        board_id = self.context.get("board_id")
        board = get_object_or_404(Board, pk=board_id)

        post = Post.objects.create(writer=user, board=board, **validated_data)
        return post

    def update(self, post, validated_data):
        post.title = validated_data.get("title", post.title)
        post.content = validated_data.get("content", post.content)
        post.is_anonymous = validated_data.get("is_anonymous", post.is_anonymous)
        post.save()
        return post


class PostSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "writer",
            "is_anonymous",
            "created_at",
            "updated_at",
        )

    def get_writer(self, post):
        if post.is_anonymous:
            return "익명"
        else:
            return post.writer.name


class CommentCreateSerializer(serializers.Serializer):
    pass