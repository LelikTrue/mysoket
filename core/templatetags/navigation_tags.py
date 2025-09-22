# Path: core/templatetags/navigation_tags.py

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active_nav(context, *url_names):
    """
    Проверяет, является ли текущая страница активной для навигации.
    Принимает одно или несколько имен URL (url_names).
    Возвращает 'active' если текущий URL относится к одному из имен,
    иначе возвращает пустую строку.
    """
    request = context['request']
    current_url_name = request.resolver_match.url_name
    
    # Проверяем, начинается ли имя текущего URL с одного из префиксов
    for name in url_names:
        if current_url_name.startswith(name):
            return 'active'
            
    return ''