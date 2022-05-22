from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from board.models import Post
from board.serializers import PostCreateSerializer


class PostViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()

    def create(self, request, b_id):
        user = request.user
        serializer = PostCreateSerializer(
            data=request.data, context={"user": user, "board_id": b_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
