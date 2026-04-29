from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?7?\d{10}$',
        message="Номер телефона должен быть в формате: '+71234567890' или '81234567890'"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name='Номер телефона'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number