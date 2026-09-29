from django.conf import settings
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="users_joined", blank=True
    )

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="chat_messages",
    )
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.PROTECT,
        related_name="chat_messages",
    )
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.chat_room} at {self.sent_on}"
