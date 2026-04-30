from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/video/', views.stream_lesson_video, name='stream_lesson_video'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),   # <-- должно быть здесь
]