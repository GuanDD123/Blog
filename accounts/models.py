from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    following = models.ManyToManyField(
        "self",
        through="Contact",
        related_name="followers",
        symmetrical=False,
    )

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})


class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contacts_from"
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contacts_to"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = (models.Index(fields=["-created_at"]),)
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="users/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
