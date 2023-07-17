from django.urls import path
from .views import *

from django.conf.urls.static import static

from Foody import settings

urlpatterns = [
    path('', main, name='main'),
    path('aboutus/', about_us, name='about_us'),
    path('contacts/', ContactFormView.as_view(), name='contacts'),
    path('catalog/', recipe_catalog, name='catalog'),
    path('sign_in/', LoginUser.as_view(), name='sign_in'),
    path('sign_up/', RegisterUser.as_view(), name='sign_up'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('my_recipes/', my_recipes, name='my_recipes'),
    path('category/<slug:cat_slug>/',recipe_category, name='category'),
    path('recipe/<slug:rec_slug>/', show_recipe, name='recipe'),
    path('update_recipe/<slug:rec_slug>/', update_recipe, name='update_recipe'),
    path('add_recipe/', add_recipe, name='add_recipe'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
