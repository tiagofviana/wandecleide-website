from django import template
from django.utils import translation
from django.urls import resolve, reverse

register = template.Library()


@register.simple_tag(name='translate_current_url', takes_context=True)
def translate_url(context, language_code: str):
    view = resolve(context['request'].path)
    request_language = translation.get_language()
    translation.activate(language_code)
    url = reverse(f"{view.app_name}:{view.url_name}", args=view.args, kwargs=view.kwargs)
    translation.activate(request_language)
    return url




class TranslatedURL(template.Node):
    def __init__(self, language: str):  
        self.language = language

    def render(self, context):
        view = resolve(context['request'].path)
        request_language = translation.get_language()
        translation.activate(self.language)
        url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        translation.activate(request_language)
        return url