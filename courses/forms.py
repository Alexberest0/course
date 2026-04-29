from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=17,
        label='Номер телефона',
        widget=forms.TextInput(attrs={'placeholder': '+71234567890'})
    )

    class Meta:
        model = User
        fields = ('phone_number', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': '+71234567890'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)