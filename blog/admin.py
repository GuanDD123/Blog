from typing import ClassVar

from django.contrib import admin

from actions.utils import export_to_csv

from .models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "status", "published_at")
    list_filter = ("status", "created_at", "updated_at", "published_at", "author")
    search_fields = ("title", "content")
    date_hierarchy = "published_at"
    ordering = ("status", "-published_at")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("title",)}
    autocomplete_fields = ("author",)
    inlines = (CommentInline,)
    actions = (export_to_csv,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "content", "created_at", "active")
    list_filter = ("active", "created_at", "updated_at")
    search_fields = ("user", "content")
    autocomplete_fields = ("user", "post")
    actions = (export_to_csv,)
