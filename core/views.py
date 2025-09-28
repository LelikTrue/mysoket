# Path: core/views.py

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Service, Page, Article, Category, Tag 

# --- Основные Views ---

def home_view(request):
    """Отображает главную страницу со списком всех услуг."""
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'core/home.html', context)

def service_detail_view(request, service_slug):
    """Отображает детальную страницу для одной услуги."""
    service = get_object_or_404(Service, slug=service_slug)
    context = {'service': service}
    return render(request, 'core/service_detail.html', context)

def page_view(request, page_slug):
    """Отображает любую статическую страницу, созданную в админке."""
    page = get_object_or_404(Page, slug=page_slug, is_published=True)
    context = {'page': page}
    return render(request, page.template, context)

# --- Views для Статей ---

def article_list_view(request):
    all_articles = Article.objects.filter(is_published=True).order_by('-published_date')
    page_title = 'Статьи'

    query = request.GET.get('q')
    if query:
        all_articles = all_articles.filter(Q(title__iregex=query) | Q(content__iregex=query))
        page_title = f'Результаты поиска по запросу: "{query}"'

    paginator = Paginator(all_articles, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': page_title,
        'all_tags': Tag.objects.all(),
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/partials/article_list_partial.html', context)
    return render(request, 'core/article_list.html', context)

def article_detail_view(request, post_slug):
    post = get_object_or_404(Article, slug=post_slug, is_published=True)
    
    # <<< НАЧАЛО: Логика для похожих статей
    related_posts = Article.objects.none() # Создаем пустой QuerySet по умолчанию
    if post.category:
        related_posts = Article.objects.filter(
            category=post.category, 
            is_published=True
        ).exclude(
            pk=post.pk
        )[:4] # Исключаем текущую статью и берем 4 похожих
    # <<< КОНЕЦ: Логика для похожих статей

    context = {
        'post': post,
        'related_posts': related_posts, # <<< Добавляем в контекст
    }
    return render(request, 'core/article_detail.html', context)

def article_category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    all_articles = Article.objects.filter(category=category, is_published=True).order_by('-published_date')
    
    # Получаем уникальный набор тегов, которые принадлежат ТОЛЬКО статьям из этой категории
    tags_for_category = Tag.objects.filter(posts__in=all_articles).distinct()

    paginator = Paginator(all_articles, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': f'Статьи по категории: {category.name}',
        'all_tags': tags_for_category, # <-- Передаем в контекст отфильтрованный список
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/partials/article_list_partial.html', context)
    return render(request, 'core/article_list.html', context)

def article_tag_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    all_articles = Article.objects.filter(tags=tag, is_published=True).order_by('-published_date')

    # Получаем уникальный набор тегов, которые принадлежат ТОЛЬКО статьям с текущим тегом
    tags_for_articles = Tag.objects.filter(posts__in=all_articles).distinct()
    # -------------------------

    paginator = Paginator(all_articles, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': f'Статьи по тегу: {tag.name}',
        'all_tags': tags_for_articles, # <-- Передаем в контекст отфильтрованный список
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/partials/article_list_partial.html', context)
    return render(request, 'core/article_list.html', context)

# --- API Views ---

def article_search_api_view(request):
    """API v1: Поиск по заголовкам статей для "живого" поиска."""
    query = request.GET.get('q', '')
    articles_qs = Article.objects.none()
    
    if len(query) > 2:
        articles_qs = Article.objects.filter(
            is_published=True,
            title__iregex=query
        ).distinct()[:5]

    results = []
    for post in articles_qs:
        content_preview = post.content.replace('##', '').replace('###', '').strip()
        excerpt = content_preview[:70] + '...' if len(content_preview) > 70 else content_preview

        results.append({
            'title': post.title,
            'url': post.get_absolute_url(),
            'excerpt': excerpt,
        })
        
    response_data = {
        'count': len(results),
        'results': results,
    }
            
    return JsonResponse(response_data)