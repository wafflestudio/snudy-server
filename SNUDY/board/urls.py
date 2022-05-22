from rest_framework.routers import SimpleRouter

from django.urls import path, include

from board.views import PostViewSet, CommentViewSet


app_name = "board"
router = SimpleRouter()
router.register(
    "board/(?P<b_pk>[0-9]+)/post", PostViewSet, basename="post"
)  # /api/v1/board/<b_pk>/post/
router.register(
    "board/(?P<b_pk>[0-9]+)/post/(?P<p_pk>[0-9]+)/comment",
    CommentViewSet,
    basename="comment",
)  # /api/v1/board/<b_pk>/post/<p_pk>/comment/

urlpatterns = [
    path("", include(router.urls)),
]
