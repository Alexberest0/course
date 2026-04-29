from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView  # Импортируем класс для перенаправления

urlpatterns = [
    # Эта новая строчка перенаправит пользователя с главной страницы сайта
    # прямо на страницу входа в ваше приложение courses.
    path('', RedirectView.as_view(url='/courses/login/', permanent=False), name='root-redirect'),

    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
]