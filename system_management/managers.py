from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and returns a superuser with the specified email, password, and extra fields.

        Args:
            email (str): The email address for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created superuser instance.

        Raises:
            ValueError: If 'is_staff' is not set to True in extra_fields.
            ValueError: If 'is_superuser' is not set to True in extra_fields.

        Notes:
            The method ensures that the superuser has 'is_staff', 'is_superuser', and 'is_active'
            set to True before calling the 'create_user' method.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)