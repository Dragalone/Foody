from  django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('aboutus/', about_us, name='about_us'),
    path('contacts/', contacts, name='contacts'),
    path('catalog/', catalog, name='catalog'),
]