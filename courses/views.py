from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm

# Функция для отображения каталога курсов (заглушка)
def catalog(request):
    demo_courses = [
        {'id': 1, 'title': 'Основы Python', 'description': 'Изучите Python с нуля'},
        {'id': 2, 'title': 'Django для начинающих', 'description': 'Создайте свой первый сайт'},
        {'id': 3, 'title': 'Водяные знаки в видео', 'description': 'Защитите свой контент'},
    ]
    return render(request, 'courses/catalog.html', {'courses': demo_courses})

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