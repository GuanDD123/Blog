import markdown
from django import template
from django.core.cache import cache
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag
def posts_published_count():
    return Post.published.count()


@register.inclusion_tag("blog/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-published_at")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commended_posts(count=5):
    most_commended = cache.get("most_commended_posts")
    if most_commended is None:
        most_commended = Post.published.annotate(
            total_comments=Count("comments")
        ).order_by("-total_comments")[:count]
        cache.set("most_commended_posts", most_commended, 5 * 60)
    return most_commended


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
