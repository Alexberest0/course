from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
import uuid

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
    
    # НОВОЕ поле – публичный уникальный идентификатор
    public_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='Публичный ID')
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Если public_id не задан – генерируем
        if not self.public_id:
            self.public_id = uuid.uuid4().hex  # например: 'e1a2b3c4d5e6f7890abcdef12345678' (32 символа)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number
    


    


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название курса')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name='Обложка')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название урока')
    video = models.FileField(upload_to='lessons/', verbose_name='Видеофайл')
    description = models.TextField(blank=True, verbose_name='Описание урока')
    pdf_file = models.FileField(upload_to='lesson_pdfs/', blank=True, null=True, verbose_name='PDF файл')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    

class AccessCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_courses')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='purchased_by')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')