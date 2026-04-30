from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Lesson   # добавили Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}   # автоматически заполнять slug из title
    list_display = ('title', 'price', 'created_at')
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')   # добавили course
    list_filter = ('course',)   # фильтр по курсу
    fields = ('course', 'title', 'video', 'description', 'pdf_file', 'order')

class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'public_id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'public_id', 'username', 'email')
    readonly_fields = ('public_id',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('public_id',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

admin.site.register(User, CustomUserAdmin)