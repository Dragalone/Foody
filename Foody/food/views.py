from django.shortcuts import render

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

def sign_in (request):
    context = {
        'title': 'Регистрация',
    }
    return render(request, 'food/sign_in.html', context=context)

def sign_up (request):
    context = {
        'title': 'Вход',
    }
    return render(request, 'food/sign_up.html', context=context)