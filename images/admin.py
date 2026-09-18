from typing import ClassVar

from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "image", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("title",)}
