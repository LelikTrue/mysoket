# Path: myproject/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# 1. Импортируем sitemap view и наши классы Sitemap
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ArticleSitemap, ServiceSitemap, StaticViewSitemap, PageSitemap

# 2. Собираем все классы Sitemap в один словарь
sitemaps = {
    'static': StaticViewSitemap,
    'pages': PageSitemap, 
    'services': ServiceSitemap,
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 3. Добавляем маршрут для sitemap.xml
    # Django будет использовать view 'sitemap' и наш словарь 'sitemaps' для генерации файла
    path(
        'sitemap.xml', 
        sitemap, 
        {'sitemaps': sitemaps}, 
        name='django.contrib.sitemaps.views.sitemap'
    ),
    
    # Основные маршруты нашего приложения core
    path('', include('core.urls')),
]

# Этот блок нужен для корректной отдачи медиафайлов в режиме разработки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)