from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView

class MessagesTemplateView(TemplateView):
    template_name='core/messages.html'

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.session.get(settings.SESSION_REDIRECT_URL, None)

        if context['url']:
            del self.request.session[settings.SESSION_REDIRECT_URL]

        return context
    