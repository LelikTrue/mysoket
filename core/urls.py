# Path: core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Маршруты для главной страницы и услуг
    path('', views.home_view, name='home'),
    path('service/<slug:service_slug>/', views.service_detail_view, name='service_detail'),
    
    # Маршруты для статей (приведены к единому стилю)
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<slug:post_slug>/', views.article_detail_view, name='article_detail'),
    path('articles/category/<slug:category_slug>/', views.article_category_view, name='article_category'),
    path('articles/tag/<slug:tag_slug>/', views.article_tag_view, name='article_tag'),
    
    # API маршрут для "живого" поиска
    path('api/v1/articles/search/', views.article_search_api_view, name='api_v1_article_search'),
    
    # "Умный" маршрут для статических страниц (остается последним)
    path('<slug:page_slug>/', views.page_view, name='page_view'),
]