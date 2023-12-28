from django.conf import settings
from django.http import HttpResponse


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: HttpResponse = self.get_response(request)

        print('\n\n')

        csp_rules = settings.CSP_RULES.replace("\n", "")
        response.headers['Content-Security-Policy'] = csp_rules

        return response