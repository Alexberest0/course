from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Lesson
from django.shortcuts import render, redirect, get_object_or_404



import os
import re
from django.http import HttpResponse, Http404, HttpResponseNotModified
from django.views.static import serve
from django.conf import settings
from .models import Course   # в начале файла добавьте импорт

def catalog(request):
    courses = Course.objects.all()  # получаем все курсы из БД
    return render(request, 'courses/catalog.html', {'courses': courses})

# Функция для отображения каталога курсов (заглушка)
def catalog(request):
    courses = Course.objects.all()  # получаем все курсы из БД
    return render(request, 'courses/catalog.html', {'courses': courses})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = UserRegistrationForm()
    return render(request, 'courses/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                # Если пользователь - суперпользователь, то в админку
                if user.is_superuser:
                    return redirect('/admin/')
                else:
                    return redirect('catalog')
    else:
        form = UserLoginForm()
    return render(request, 'courses/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def lesson_detail(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        raise Http404("Урок не найден")
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})



@login_required
def stream_lesson_video(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        video_path = lesson.video.path
    except (Lesson.DoesNotExist, ValueError):
        raise Http404("Урок или видео не найдены")

    # Проверяем, существует ли файл
    if not os.path.exists(video_path):
        raise Http404("Файл видео отсутствует")

    # Открываем файл в бинарном режиме
    file_handle = open(video_path, 'rb')
    
    # Получаем размер файла
    stat = os.stat(video_path)
    file_size = stat.st_size
    
    # Заголовки по умолчанию
    response_headers = {
        'Content-Type': 'video/mp4',
        'Accept-Ranges': 'bytes',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
    }
    
    # Обрабатываем Range-заголовок (для перемотки)
    range_header = request.headers.get('Range', None)
    if range_header:
        # Ищем байтовый диапазон: bytes=start-end
        m = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if m:
            start = int(m.group(1))
            end = m.group(2)
            if end:
                end = int(end)
            else:
                end = file_size - 1
            # Проверяем границы
            if start >= file_size or end >= file_size:
                return HttpResponse(status=416)  # Requested Range Not Satisfiable
            # Устанавливаем позицию в файле
            file_handle.seek(start)
            # Читаем нужный кусок
            data = file_handle.read(end - start + 1)
            response_headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response_headers['Content-Length'] = str(end - start + 1)
            return HttpResponse(data, status=206, headers=response_headers)
    
    # Если нет range, отдаём весь файл
    response_headers['Content-Length'] = str(file_size)
    return HttpResponse(file_handle.read(), status=200, headers=response_headers)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    user_has_access = False

    # Проверяем, есть ли у пользователя уже доступ (для бесплатных курсов или админа)
    if request.user.is_authenticated:
        if request.user.is_superuser or course.price == 0:
            user_has_access = True

    # Обработка промокода (временная логика)
    promo_code = request.POST.get('promo_code') if request.method == 'POST' else None
    if promo_code == 'TESTCODE':  # простой промокод для теста
        user_has_access = True
        # Здесь можно сохранить факт активации в сессию или базу, но для теста просто даём доступ на текущий запрос

    lessons = course.lessons.all() if user_has_access else None

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'user_has_access': user_has_access,
        'lessons': lessons,
    })