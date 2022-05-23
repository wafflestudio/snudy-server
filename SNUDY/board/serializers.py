from requests import request
from rest_framework import serializers

from django.shortcuts import get_object_or_404

from board.models import Post, Board, Comment


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    is_anonymous = serializers.BooleanField(required=False)

    def validate(self, data):
        writer = self.context.get("writer")
        if writer is None:
            raise serializers.ValidationError()

        board_id = self.context.get("board_id")
        board = get_object_or_404(Board, pk=board_id)
        return data

    def create(self, validated_data):
        writer = self.context.get("writer")
        board_id = self.context.get("board_id")
        board = get_object_or_404(Board, pk=board_id)

        post = Post.objects.create(writer=writer, board=board, **validated_data)
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


class PostSimpleSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
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
    parent_id = serializers.IntegerField(required=False)
    content = serializers.CharField(max_length=255)
    is_anonymous = serializers.BooleanField(required=False)

    def validate(self, data):
        writer = self.context.get("writer")
        if writer is None:
            raise serializers.ValidationError()

        post_id = self.context.get("post_id")
        post = get_object_or_404(Post, pk=post_id)

        parent_id = data.get("parent_id")
        if parent_id is not None:
            parent = get_object_or_404(Comment, pk=parent_id)
        return data

    def create(self, validated_data):
        writer = self.context.get("writer")
        post_id = self.context.get("post_id")
        post = get_object_or_404(Post, pk=post_id)

        comment = Comment.objects.create(writer=writer, post=post, **validated_data)
        return comment

    def update(self, comment, validated_data):
        comment.content = validated_data.get("content", comment.content)
        comment.is_anonymous = validated_data.get("is_anonymous", comment.is_anonymous)
        comment.save()
        return comment


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)
    parent_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "writer",
            "parent_id",
            "content",
            "is_anonymous",
            "created_at",
            "updated_at",
        )

    def get_writer(self, comment):
        if comment.is_anonymous:
            return "익명"
        else:
            return comment.writer.name

    def get_parent_id(self, comment):
        if comment.parent is None:
            return None
        else:
            return comment.parent.id
