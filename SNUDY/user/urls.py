from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user.views import UserLoginView, UserSignUpView

router = SimpleRouter()

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),  # /api/v1/signup/
    path("login/", UserLoginView.as_view(), name="login"),  # /api/v1/login/
    path("", include(router.urls)),
]
