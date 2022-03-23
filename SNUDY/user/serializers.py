from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# user -> jwt_token
def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token


class UserCreateSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=128, required=True)
    name = serializers.CharField(max_length=32, required=True)
    password = serializers.CharField(max_length=32, required=True)

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=email, password=password, **validated_data
        )
        return user, jwt_token_of(user)


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(max_length=32, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Wrong Information")

        update_last_login(None, user)
        return {"email": user.email, "token": jwt_token_of(user)}
