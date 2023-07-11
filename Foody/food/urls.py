from  django.urls import path
from .views import *
from Foody import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', main, name='main'),
    path('aboutus/', about_us, name='about_us'),
    path('contacts/', contacts, name='contacts'),
    path('catalog/', catalog, name='catalog'),
    path('sign_in/', LoginUser.as_view(), name='sign_in'),
    path('sign_up/', RegisterUser.as_view(), name='sign_up'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)