# Path: core/context_processors.py

from django.conf import settings
from django.contrib.sites.models import Site

def debug(request):
    """
    Передает переменную settings.DEBUG в контекст каждого шаблона.
    Это позволяет использовать в шаблонах конструкцию типа {% if debug %}.
    """
    return {'debug': settings.DEBUG}

def site_info(request):
    """
    Добавляет в контекст объект текущего сайта (из Sites Framework).
    Это позволяет в шаблонах обращаться к домену через {{ site.domain }}.
    """
    return {'site': Site.objects.get_current()}