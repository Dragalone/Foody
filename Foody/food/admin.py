from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Recipe_block)
admin.site.register(Category)

