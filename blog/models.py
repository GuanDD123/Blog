from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = ("DF", "Draft")
        PUBLISHED = ("PB", "Published")

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date="published_at")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-published_at",)
        indexes = (models.Index(fields=["-published_at"]),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            kwargs={
                "year": self.published_at.year,
                "month": self.published_at.month,
                "day": self.published_at.day,
                "slug": self.slug,
            },
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)
        indexes = (models.Index(fields=["created_at"]),)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
