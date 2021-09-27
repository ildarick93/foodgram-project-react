from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class UserRoles:
    USER = 'user'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (ADMIN, ADMIN),
    )


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, blank=False)
    password = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        # 'username',
        'password',
        'email',
        'first_name',
        'last_name'
    ]
    objects = CustomUserManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER
