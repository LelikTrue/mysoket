# Path: E:\python-Prog\it_solutions_hub\core\context_processors.py
from django.conf import settings

def debug(request):
    """
    Передает переменную settings.DEBUG в контекст каждого шаблона.
    Это позволяет использовать в шаблонах конструкцию типа {% if debug %}.
    """
    return {'debug': settings.DEBUG}