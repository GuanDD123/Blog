from typing import ClassVar

from django.contrib import admin

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
    ordering = ("status", "published_at")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("title",)}
    autocomplete_fields = ("author",)
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post", "created_at", "active")
    list_filter = ("active", "created_at", "updated_at")
    search_fields = ("name", "email", "content")
