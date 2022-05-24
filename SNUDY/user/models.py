from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = "email"

    email = models.EmailField(max_length=128, unique=True)
    name = models.CharField(max_length=32)
    student_id = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_admin = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=True)

    objects = CustomUserManager()
