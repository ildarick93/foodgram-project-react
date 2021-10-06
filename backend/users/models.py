from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    USER = 'user'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (ADMIN, ADMIN),
    )


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )

    class Meta(AbstractUser.Meta):
        ordering = ['username']

    def __str__(self):
        return self.get_full_name()

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER


User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed'
    )

    class Meta:
        ordering = ['user']
        unique_together = ['user', 'author']

    def __str__(self):
        return f'{self.user} follows {self.author}'
