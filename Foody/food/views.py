from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, UserUpdateForm, ProfileUpdateForm, AddBlockForm, AddRecipeForm, \
    UpdateRecipeForm, UpdateBlockForm, ContactForm
from .models import Recipe, Category, Recipe_block
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
@login_required(login_url='sign_in')
def my_recipes(request):

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
        recipes = Recipe.objects.filter(is_published=True,title__contains=name_searched,user=request.user)
        cats = Category.objects.annotate(Count('recipe')).filter(name__contains=cat_searched)
        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,
            'page_obj': page_obj,
        }
        return render(request, 'food/my_recipes.html', context=context)
    else:
        recipes = Recipe.objects.filter(is_published=True,user=request.user).select_related('cat')
        cats = Category.objects.annotate(Count('recipe'))
        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,
            'cat_selected': 0,
            'page_obj': page_obj,
        }
        return render(request, 'food/my_recipes.html', context=context)


@login_required(login_url='sign_in')
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
        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,
            'page_obj': page_obj,
        }
        return render(request, 'food/catalog.html', context=context)
    else:
        recipes = Recipe.objects.filter(is_published=True).select_related('cat')
        cats = Category.objects.annotate(Count('recipe'))
        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,
            'cat_selected': 0,
            'page_obj': page_obj,
        }
        return render(request, 'food/catalog.html', context=context)


@login_required(login_url='sign_in')
def recipe_category(request,cat_slug):
    if request.method == "POST":
        if 'name_searched' in request.POST:
            name_searched = request.POST['name_searched']
        else:
            name_searched = ""
        if 'cat_searched' in request.POST:
            cat_searched = request.POST['cat_searched']
        else:
            cat_searched = ""

        recipes = Recipe.objects.filter(is_published=True,cat__slug=cat_slug,title__contains=name_searched)
        cats = Category.objects.annotate(Count('recipe')).filter(name__contains=cat_searched)
        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,
            'cat_selected': cat_slug,
            'page_obj': page_obj,
        }
        return render(request, 'food/catalog.html', context=context)
    else:
        recipes = Recipe.objects.filter(is_published=True,cat__slug=cat_slug).select_related('cat')
        cats = Category.objects.annotate(Count('recipe'))
        paginator = Paginator(recipes, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'title': 'Каталог',
            'recipes' : recipes,
            'cats' : cats,
            'cat_selected': cat_slug,
            'page_obj': page_obj,
        }
        return render(request, 'food/catalog.html', context=context)


def show_recipe(request,rec_slug):
    recipe = get_object_or_404(Recipe, slug=rec_slug)
    blocks = recipe.recipe_block_set.all()
    context = {
        'title': recipe.title,
        'r': recipe,
        'blocks': blocks,
    }
    return render(request, 'food/recipe.html', context=context)


def add_recipe(request):
    if request.method == 'POST':
        recipe_form = AddRecipeForm(request.POST, request.FILES, user=request.user, slug='-1')
        block_form1 = AddBlockForm(request.POST, request.FILES, recipe=None,prefix='block_form1')
        block_form2 = AddBlockForm(request.POST, request.FILES, recipe=None,prefix='block_form2')
        block_form3 = AddBlockForm(request.POST, request.FILES, recipe=None,prefix='block_form3')
        if recipe_form.is_valid() and block_form1.is_valid() and block_form2.is_valid() and block_form3.is_valid():
            recipe_form.save()
            rec = Recipe.objects.latest()
            block_form1 = AddBlockForm(request.POST, request.FILES, recipe=rec,prefix='block_form1')
            block_form2 = AddBlockForm(request.POST, request.FILES, recipe=rec,prefix='block_form2')
            block_form3 = AddBlockForm(request.POST, request.FILES, recipe=rec,prefix='block_form3')
            block_form1.save()
            block_form2.save()
            block_form3.save()
            return redirect('catalog')
    else:
        recipe_form = AddRecipeForm(user=request.user, slug='-1')
        block_form1 = AddBlockForm( recipe=None,prefix='block_form1')
        block_form2 = AddBlockForm( recipe=None,prefix='block_form2')
        block_form3 = AddBlockForm(recipe=None,prefix='block_form3')
    return render(request, 'food/add_recipe.html', {'block_form1':block_form1,'block_form2':block_form2,'block_form3':block_form3,'recipe_form':recipe_form, 'title': 'Добавление рецепта'})

def update_recipe(request, rec_slug):
    recipe = get_object_or_404(Recipe, slug=rec_slug)
    blocks = recipe.recipe_block_set.all()

    if request.method == 'POST':
        recipe_form = UpdateRecipeForm(request.POST, request.FILES, instance=recipe)
        block_form1 = UpdateBlockForm(request.POST, request.FILES, instance=blocks[0],prefix='block_form1')
        block_form2 = UpdateBlockForm(request.POST, request.FILES, instance=blocks[1],prefix='block_form2')
        block_form3 = UpdateBlockForm(request.POST, request.FILES, instance=blocks[2],prefix='block_form3')
        if recipe_form.is_valid() and block_form1.is_valid() and block_form2.is_valid() and block_form3.is_valid():
            recipe_form.save()
            block_form1.save()
            block_form2.save()
            block_form3.save()
            return redirect('catalog')
    else:
        recipe_form = UpdateRecipeForm(instance=recipe)
        block_form1 = UpdateBlockForm(instance=blocks[0],prefix='block_form1')
        block_form2 = UpdateBlockForm(instance=blocks[1],prefix='block_form2')
        block_form3 = UpdateBlockForm(instance=blocks[2],prefix='block_form3')


    context = {
        'r': recipe,
        'blocks': blocks,'block_form1':block_form1,
        'block_form2':block_form2,
        'block_form3':block_form3,
        'recipe_form':recipe_form,
        'title': 'Изменение рецепта'
    }
    return render(request, 'food/update_recipe.html', context=context)

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'food/contacts.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('main')