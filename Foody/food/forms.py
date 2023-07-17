from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import formset_factory

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
        label='Имя',
        max_length=100,
        help_text='Введите имя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        help_text='Введите фамилию',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Фамилия'}),
    )
    username = forms.CharField(
        label='Имя пользователя',
        max_length=200,
        help_text='Введите имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя пользователя'}),
    )
    email = forms.EmailField(
        label='Адрес электронной почты',
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
        widget=forms.FileInput(attrs={'class': 'form-control form-control-lg', 'id': 'userAvatar', 'size' : '50', 'type':'file'}),
    )
    class Meta:
        model = Profile
        fields = ('avatar',)





class AddBlockForm(forms.ModelForm):
    photo = forms.ImageField(
        label='Фото',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control','required': 'True'}),
    )
    def __init__(self, *args, **kwargs):
        self._recipe = kwargs.pop('recipe')
        super(AddBlockForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        inst = super(AddBlockForm, self).save(commit=False)
        inst.recipe = self._recipe
        if commit:
            inst.save()
            self.save_m2m()
        return inst


    class Meta:
        model = Recipe_block
        fields = ['content', 'photo']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control','cols': 60, 'rows': 10,'placeholder': 'Введите описание рецепта'}),
        }

class AddRecipeForm(forms.ModelForm):
    preview_photo = forms.ImageField(
        label='Добавить превью',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control','required': 'True'}),
    )
    is_published = forms.BooleanField(
        required=False,
        label='Опубликовать',
    )
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._slug = kwargs.pop('slug')
        super(AddRecipeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(AddRecipeForm, self).save(commit=False)
        inst.user = self._user
        inst.slug = self._slug
        if commit:
            inst.save()
            self.save_m2m()
        return inst
    class Meta:
        model = Recipe
        fields = ['title', 'cat', 'is_published', 'preview_photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }



class UpdateBlockForm(forms.ModelForm):
    photo = forms.ImageField(
        label='Фото',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    def __init__(self, *args, **kwargs):
        super(UpdateBlockForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = ('recipe',)
        model = Recipe_block
        fields = ['content', 'photo']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control','cols': 60, 'rows': 10,'placeholder': 'Введите описание рецепта'}),
        }

class UpdateRecipeForm(forms.ModelForm):
    preview_photo = forms.ImageField(
        label='Добавить превью',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    is_published = forms.BooleanField(
        label='Опубликовать',
        required=False,
        widget=forms.CheckboxInput(attrs={'class':'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super(UpdateRecipeForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = ('user', 'slug')
        model = Recipe
        fields = ['title', 'cat', 'is_published', 'preview_photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'},),

        }

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя'}),)
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'email'}),)
    content = forms.CharField(label='Сообщение',widget=forms.Textarea(attrs={'class': 'form-control','cols': 60, 'rows': 10, 'placeholder': 'Сообщение'}),)
    captcha = CaptchaField(label='Введите',widget=CaptchaTextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите'}),)
