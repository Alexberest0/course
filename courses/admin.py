from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Стандартные поля, которые будут отображаться в списке пользователей
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'username', 'email', 'is_staff', 'is_active')
    # Поле, по которому будет происходить поиск в админке
    search_fields = ('phone_number', 'username', 'email')
    # Поле, используемое для входа в систему (оно будет на странице добавления пользователя)
    USERNAME_FIELD = 'phone_number'

# Регистрируем нашу модель с нашими настройками
admin.site.register(User, CustomUserAdmin)