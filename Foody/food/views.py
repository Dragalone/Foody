from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, UserUpdateForm, ProfileUpdateForm
from .models import Recipe, Category
from .utils import DataMixin
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.db.models import Count, Q


# Create your views here.

def main (request):
    context = {
        'title': 'Foody',
    }
    return render(request, 'food/main.html', context=context)

def about_us (request):
    context = {
        'title': 'О разработчике',
    }
    return render(request, 'food/about_us.html', context=context)

def contacts (request):
    context = {
        'title': 'Обратная связь',
    }
    return render(request, 'food/contacts.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('main')



class RegisterUser(CreateView, DataMixin):
    form_class = RegisterUserForm
    template_name = 'food/sign_up.html'
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'food/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')

@login_required(login_url='sign_in')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Профиль',
    }
    return render(request, 'food/profile.html',context)

def my_recipes(request):
    context = {
        'title': 'Мои рецепты',
    }
    return render(request, 'food/my_recipes.html',context)

class RecipeCategory(DataMixin, ListView):
    model = Recipe
    template_name = 'food/catalog.html'
    context_object_name = 'recipes'
    allow_empty = False

    def get_queryset(self):
        return Recipe.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


def recipe_catalog(request):

    if request.method == "POST":
        if 'name_searched' in request.POST:
            name_searched = request.POST['name_searched']
        else:
            name_searched = ""
        if 'cat_searched' in request.POST:
            cat_searched = request.POST['cat_searched']
        else:
            cat_searched = ""
        print("cat_searched: ")
        print(cat_searched)
        recipes = Recipe.objects.filter(is_published=True,title__contains=name_searched)
        cats = Category.objects.annotate(Count('recipe')).filter(name__contains=cat_searched)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,

        }
        return render(request, 'food/catalog.html', context=context)
    else:
        recipes = Recipe.objects.filter(is_published=True).select_related('cat')
        cats = Category.objects.annotate(Count('recipe'))
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats
        }
        return render(request, 'food/catalog.html', context=context)

class RecipeCatalog(DataMixin, ListView):
    model = Recipe
    template_name = 'food/catalog.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Каталог')
        return dict(list(context.items()) + list(c_def.items()))

class ShowRecipe(DataMixin, DetailView):
    model = Recipe
    template_name = 'food/recipe.html'
    slug_url_kwarg = 'recipe_slug'
    context_object_name = 'recipe'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['recipe'])
        return dict(list(context.items()) + list(c_def.items()))