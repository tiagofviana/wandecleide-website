from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.utils import timezone

class PrioritySiteMap(Sitemap):
    changefreq = 'daily'
    protocol = 'https'
    priority = 1
    lastmod = timezone.now()
    i18n=True

    def items(self):
        return ['users:index']

    def location(self, item):
        return reverse(item)


class OthersSiteMap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'
    priority = 0.5
    lastmod = timezone.now()
    i18n=True

    def items(self):
        return ['about', 'contact']

    def location(self, item):
        return reverse(f'users:{item}')
    
SITEMAPS = {
    'priority' : PrioritySiteMap,
    'others': OthersSiteMap,
}
