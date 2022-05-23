from os import stat
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from board.models import Board, Post, Comment
from board.serializers import (
    PostCreateSerializer,
    PostSerializer,
    PostSimpleSerializer,
    CommentCreateSerializer,
    CommentSerializer,
)


class PostViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, b_pk=None):
        board = get_object_or_404(Board, pk=b_pk)
        all_posts = self.queryset.filter(board=board)
        all_posts = all_posts.order_by('-created_at')

        paginator = Paginator(all_posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return Response(data=PostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)


    def create(self, request, b_pk=None):
        user = request.user
        serializer = PostCreateSerializer(
            data=request.data, context={"writer": user, "board_id": b_pk}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(
            data=self.get_serializer(post).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None, **kwargs):
        post = get_object_or_404(self.queryset, pk=pk)
        return Response(data=self.get_serializer(post).data, status=status.HTTP_200_OK)

    def update(self, request, b_pk=None, pk=None):
        user = request.user
        post = get_object_or_404(self.queryset, pk=pk)
        if user != post.writer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PostCreateSerializer(
            post, data=request.data, context={"writer": user, "board_id": b_pk}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(data=self.get_serializer(post).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):
        user = request.user
        post = get_object_or_404(self.queryset, pk=pk)
        if user != post.writer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request, p_pk=None, **kwargs):
        post = get_object_or_404(Post, pk=p_pk)
        comments = self.queryset.filter(post=post)
        comments = comments.order_by("created_at")
        return Response(
            data=self.get_serializer(comments, many=True).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request, p_pk=None, **kwargs):
        user = request.user
        serializer = CommentCreateSerializer(
            data=request.data, context={"writer": user, "post_id": p_pk}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(
            data=self.get_serializer(comment).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None, **kwargs):
        comment = get_object_or_404(self.queryset, pk=pk)
        return Response(
            data=self.get_serializer(comment).data, status=status.HTTP_200_OK
        )

    def update(self, request, p_pk=None, pk=None, **kwargs):
        user = request.user
        comment = get_object_or_404(self.queryset, pk=pk)
        if user != comment.writer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CommentCreateSerializer(
            comment, data=request.data, context={"writer": user, "post_id": p_pk}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(
            data=self.get_serializer(comment).data, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None, **kwargs):
        user = request.user
        comment = get_object_or_404(self.queryset, pk=pk)
        if user != comment.writer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_200_OK)
