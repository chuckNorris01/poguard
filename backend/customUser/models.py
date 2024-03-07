from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Password must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name ,**extra_fields)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, name, password, **extra_fields):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        extra_fields.setdefault('role', 3)
        user.save()

        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserRole(Enum):
        ADMIN = 1
        MANGER = 2
        NORMAL_USER = 3

        @classmethod
        def choices(cls):
            return [(role.value, role.name) for role in cls]
        
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField(choices=UserRole.choices(), default=UserRole.NORMAL_USER.value)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    
    def __str__(self):
        return self.email
