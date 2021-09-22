from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username,  password, email, **kwargs):
        """
        Create and save a User with the given data.
        """
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("Users must have a password")
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,  password, email, **kwargs):
        """
        Create and save a SuperUser with the given data.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if not kwargs.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not kwargs.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        if not kwargs.get('is_superuser'):
            raise ValueError('Superuser must have is_active=True.')
        return self.create_user(username, password, email, **kwargs)
