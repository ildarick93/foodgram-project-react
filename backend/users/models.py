from django.contrib.auth import get_user_model
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


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    interesting_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed'
    )

    class Meta:
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
            )
        ]

    def __str__(self):
        return f'{self.user} follows {self.interesting_author}'
