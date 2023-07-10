from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'class': 'form', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form', 'placeholder': 'Username'}),
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form', 'placeholder': 'Email'}),
    )
    password1 = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form', 'placeholder': 'Password Again'}),
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        max_length=200,
        required=True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form', 'placeholder': 'Password'}),
    )


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Name',
        max_length=100,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label='Surname',
        max_length=100,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
        label='Username',
        max_length=200,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Username'}),
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Email'}),
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email')


# class ProfileUpdateForm(forms.ModelForm):
#     avatar = forms.ImageField(
#         label='Add picture',
#         required=False,
#         widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'userAvatar', 'size' : '50', 'type':'file'}),
#     )
#     class Meta:
#         model = Profile
#         fields = ('avatar',)