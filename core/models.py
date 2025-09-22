# Path: core/models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название услуги")
    slug = models.SlugField(unique=True, verbose_name="URL-адрес (автоматически)", help_text="Используется для создания красивых URL. Например, 'nastrojka-mikrotik'.")
    icon_class = models.CharField(max_length=100, verbose_name="Класс иконки (например, 'fa-solid fa-network-wired')", help_text="Скопируйте класс с сайта FontAwesome.", blank=True)
    short_description = models.TextField(verbose_name="Краткое описание (для карточки на главной)")
    full_description = models.TextField(verbose_name="Полное описание (для отдельной страницы)", blank=True)
    original_image = models.ImageField(upload_to='services/originals/', verbose_name="Изображение для услуги", help_text="Загрузите изображение. Оно будет автоматически обрезано и оптимизировано.", blank=True, null=True)
    image_detail = ImageSpecField(source='original_image', processors=[ResizeToFill(800, 400)], format='WEBP', options={'quality': 85})
    image_thumbnail = ImageSpecField(source='original_image', processors=[ResizeToFill(400, 200)], format='WEBP', options={'quality': 80})
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки", help_text="Чем меньше число, тем выше услуга в списке.")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    meta_title = models.CharField(max_length=255, verbose_name="SEO Заголовок (Title)", blank=True, help_text="Отображается во вкладке браузера и в заголовке поисковой выдачи. Оптимальная длина ~ 60 символов. Если пусто, используется название услуги.")
    meta_description = models.TextField(verbose_name="SEO Описание (Description)", blank=True, help_text="Краткое описание страницы для поисковиков (сниппет). Оптимальная длина ~ 150-160 символов. Если пусто, используется краткое описание услуги.")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['sort_order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'service_slug': self.slug})

class Page(models.Model):
    TEMPLATE_CHOICES = [
        ("core/pages/default.html", "Универсальный шаблон"),
        ("core/pages/about.html", "О компании"),
        ("core/pages/contacts.html", "Контакты"),
    ]
    title = models.CharField("Заголовок страницы (H1)", max_length=200)
    slug = models.SlugField("URL (слаг)", max_length=200, unique=True, help_text="Короткое имя для URL, например, 'about'. Должно быть уникальным.")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name="Родительская страница")
    template = models.CharField("Шаблон для отображения", max_length=100, choices=TEMPLATE_CHOICES, default="core/pages/default.html", help_text="Выберите шаблон, который определяет внешний вид страницы.")
    
    content = models.TextField("Основной контент", blank=True, help_text="Содержимое страницы. Поддерживается Markdown.")

    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField("Опубликовано", default=True, help_text="Снимите галочку, чтобы скрыть страницу с сайта.")
    meta_title = models.CharField("SEO Заголовок (Title)", max_length=200, blank=True, help_text="Если не заполнено, будет использован основной заголовок страницы.")
    meta_description = models.TextField("SEO Описание (Description)", blank=True, help_text="Краткое описание страницы для поисковых систем.")

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['slug']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug == 'home':
            return reverse('home')
        return reverse('page_view', kwargs={'page_slug': self.slug})

class Category(models.Model):
    name = models.CharField("Название категории", max_length=100, unique=True)
    slug = models.SlugField("URL (слаг)", max_length=100, unique=True, help_text="Используется в URL, например, /articles/category/network/")

    class Meta:
        verbose_name = "Категория статей"
        verbose_name_plural = "Категории статей"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article_category', kwargs={'category_slug': self.slug})

class Tag(models.Model):
    name = models.CharField("Название тега", max_length=100, unique=True)
    slug = models.SlugField("URL (слаг)", max_length=100, unique=True, help_text="Используется в URL, например, /articles/tag/mikrotik/")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article_tag', kwargs={'tag_slug': self.slug})

class Article(models.Model):
    title = models.CharField("Заголовок статьи", max_length=200)
    slug = models.SlugField("URL (слаг)", max_length=200, unique=True)
    content = models.TextField("Содержимое статьи", help_text="Поддерживается Markdown.")
    published_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    updated_date = models.DateTimeField("Дата обновления", auto_now=True)
    is_published = models.BooleanField("Опубликовано", default=False, help_text="Поставьте галочку, чтобы опубликовать статью на сайте.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts", verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="Теги")
    original_image = models.ImageField("Изображение для статьи", upload_to='articles/originals/', blank=True, null=True)
    image_thumbnail = ImageSpecField(source='original_image', processors=[ResizeToFill(400, 250)], format='WEBP', options={'quality': 80})
    meta_title = models.CharField("SEO Заголовок (Title)", max_length=200, blank=True)
    meta_description = models.TextField("SEO Описание (Description)", blank=True)

    class Meta:
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'post_slug': self.slug})