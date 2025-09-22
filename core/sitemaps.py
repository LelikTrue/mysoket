# Path: core/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Service, Page
from django.utils import timezone # Импортируем timezone

class StaticViewSitemap(Sitemap):
    """Карта сайта для ключевых статических страниц."""
    
    def priority(self, item):
        return 1.0 if item == 'home' else 0.9

    def changefreq(self, item):
        return 'daily' if item == 'home' else 'weekly'

    def items(self):
        return ['home', 'article_list']

    def location(self, item):
        return reverse(item)
        
    def lastmod(self, item):
        # Для статических страниц возвращаем текущую дату
        return timezone.now()

class PageSitemap(Sitemap):
    """Карта сайта для страниц, созданных через модель Page."""
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        # Используем новое поле updated_date
        return obj.updated_date

class ServiceSitemap(Sitemap):
    """Карта сайта для услуг."""
    changefreq = "yearly"  # <-- ИЗМЕНЕНО с monthly на yearly
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        # Используем новое поле updated_date
        return obj.updated_date

class ArticleSitemap(Sitemap):
    """Карта сайта для опубликованных статей."""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-updated_date')

    def lastmod(self, obj):
        return obj.updated_date