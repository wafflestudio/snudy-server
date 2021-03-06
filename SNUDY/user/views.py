from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserLoginSerializer, UserCreateSerializer


User = get_user_model()


class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT, data="User Already Exists")
        return Response(
            {"user": user.email, "token": jwt_token}, status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]

        return Response(
            {"success": True, "email": email, "token": token}, status=status.HTTP_200_OK
        )
