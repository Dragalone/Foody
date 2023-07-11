from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Введите имя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Введите фамилию',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Фамилия'}),
    )
    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Введите имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя пользователя'}),
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Введите адрес электронной почты',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Адрес электронной почты'}),
    )
    password1 = forms.CharField(
        help_text='Введите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Повторите пароль'}),
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Введите имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя пользователя'}),
    )
    password = forms.CharField(
        help_text='Введите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Пароль'}),
    )


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Name',
        max_length=100,
        help_text='Введите имя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        label='Surname',
        max_length=100,
        help_text='Введите фамилию',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Фамилия'}),
    )
    username = forms.CharField(
        label='Username',
        max_length=200,
        help_text='Введите имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя пользователя'}),
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        help_text='Введите адрес электронной почты',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Адрес электронной почты'}),
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        label='Добавить изображение',
        required=False,
        widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'userAvatar', 'size' : '50', 'type':'file'}),
    )
    class Meta:
        model = Profile
        fields = ('avatar',)