from django import template
from django.utils import translation
from django.urls import resolve, reverse
from django.utils.translation import gettext as _

register = template.Library()

@register.simple_tag(takes_context=True)
def translate_current_url(context, language_code: str):
    view = resolve(context['request'].path)
    request_language = translation.get_language()
    translation.activate(language_code)
    url = reverse(f"{view.app_name}:{view.url_name}", args=view.args, kwargs=view.kwargs)
    translation.activate(request_language)
    return url

@register.simple_tag(takes_context=False)
def menu_list_items() -> tuple:
    return (
        (_('Home'), reverse('users:index')),
        (_('About'), reverse('users:about')),
        (_('My work'), reverse('users:my-work')),
        (_('Contact'), reverse('users:contact')),
    )