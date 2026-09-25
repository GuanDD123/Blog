from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="images_created",
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="images_liked", blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users_like_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = (
            models.Index(fields=["-created_at"]),
            models.Index(fields=["-users_like_count"]),
        )
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("images:detail", kwargs={"pk": self.pk, "slug": self.slug})
