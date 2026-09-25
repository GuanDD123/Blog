from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actions"
    )
    verb = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="target_obj",
        blank=True,
        null=True,
    )
    target_pk = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey("target_ct", "target_pk")

    class Meta:
        indexes = (
            models.Index(fields=["-created_at"]),
            models.Index(fields=["target_ct", "target_pk"]),
        )
        ordering = ("-created_at",)
