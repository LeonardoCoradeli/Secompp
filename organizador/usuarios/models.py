from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
from django.utils import timezone


class BaseControlModel(models.Model):
    systemSmartDelete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
    

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, password_app=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser definido.')
        if not password_app or len(password_app) != 19:
            raise ValueError('O password_app deve ser definido e ter 19 caracteres.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, password_app=password_app, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, password_app=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self.create_user(email, password, password_app, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseControlModel):
    userId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    password_app = models.CharField(max_length=19)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'password_app']

    db_table = 'organizadorEmail_customuser'

    def __str__(self):
        return self.email