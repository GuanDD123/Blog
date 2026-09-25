from django.contrib.sitemaps import Sitemap

from .models import Image


class ImageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Image.objects.all()

    def lastmod(self, obj):
        return obj.created_at
