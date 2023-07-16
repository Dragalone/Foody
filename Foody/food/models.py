from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from food.slug_formation import unique_slugify
from unidecode import unidecode

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
        ordering = ['id']

    def __str__(self):
        return self.user.username
class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preview_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Превью")
    def save(self, **kwargs):
        slug_str = unidecode(str(self.title))
        unique_slugify(self, slug_str)
        super(Recipe, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'rec_slug': self.slug})
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']
class Recipe_block(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.PROTECT, verbose_name="Рецепт")
    content = models.TextField(blank=True, verbose_name="Текст рецепта")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")

    def __str__(self):
        return self.content
    class Meta:
        verbose_name = 'Блоки рецептов'
        verbose_name_plural = 'Блоки рецептов'
        ordering = ['id']
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория", unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

