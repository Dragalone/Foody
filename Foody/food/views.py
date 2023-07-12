from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, UserUpdateForm, ProfileUpdateForm
from .utils import DataMixin


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

def catalog (request):
    context = {
        'title': 'Каталог',
    }
    return render(request, 'food/catalog.html', context=context)

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
        'title': 'Profile',
    }
    return render(request, 'food/profile.html',context)