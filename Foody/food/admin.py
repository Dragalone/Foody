from django.contrib import admin
from .models import *




class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id','cat', 'title','user','time_create','time_update','is_published','slug')
    prepopulated_fields = {'slug': ('title',)}
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Profile)
admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Recipe_block)
admin.site.register(Category, CategoriesAdmin)