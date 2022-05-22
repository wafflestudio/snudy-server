from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from board.models import Post
from board.serializers import PostCreateSerializer


class PostViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()

    def create(self, request, b_pk=None):
        user = request.user
        serializer = PostCreateSerializer(
            data=request.data, context={"user": user, "board_id": b_pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, **kwargs):
        user = request.user
        post = get_object_or_404(self.queryset, pk=pk)
        if user != post.writer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_200_OK)
