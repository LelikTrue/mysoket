# Path: core/admin.py

from django.contrib import admin
from .models import Service, Page, Category, Tag, Article 

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order')
    list_editable = ('sort_order',)
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'sort_order')
        }),
        ('Контент для страницы', {
            'fields': ('icon_class', 'original_image', 'short_description', 'full_description')
        }),
        ('Настройки SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
    )

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'template', 'is_published')
    list_filter = ('is_published', 'template')
    search_fields = ('title', 'content')
    
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'is_published')
        }),
        ('Контент и Шаблон', {
            'fields': ('template', 'content')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий статей."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ-панель для тегов статей."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админ-панель для статей статей."""
    list_display = ('title', 'category', 'author', 'published_date', 'is_published')
    list_filter = ('is_published', 'category', 'author')
    search_fields = ('title', 'content')
    
    prepopulated_fields = {'slug': ('title',)}
    
    readonly_fields = ('published_date', 'updated_date')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'is_published')
        }),
        ('Контент', {
            'fields': ('content', 'original_image', 'tags')
        }),
        ('Мета-информация', {
            'fields': ('author', 'published_date', 'updated_date')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        При сохранении статьи из админки, автоматически устанавливаем
        текущего пользователя в качестве автора.
        """
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)