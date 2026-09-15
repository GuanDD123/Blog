from typing import ClassVar

from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "status", "published_at")
    list_filter = ("status", "created_at", "updated_at", "published_at", "author")
    search_fields = ("title", "content")
    date_hierarchy = "published_at"
    ordering = ("status", "published_at")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("title",)}
    raw_id_fields = ("author",)
