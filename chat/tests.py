from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ChatRoom, Message


class ChatModelTests(TestCase):
    def test_room_and_message_string_representations(self):
        user = get_user_model().objects.create_user(
            username="speaker", password="test-pass-123"
        )
        room = ChatRoom.objects.create(name="General")
        message = Message.objects.create(
            user=user, chat_room=room, content="Hello everyone"
        )

        self.assertEqual(str(room), "General")
        self.assertEqual(str(message), f"speaker on General at {message.sent_on}")


class ChatViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="member", password="test-pass-123"
        )

    def test_chat_requires_login(self):
        response = self.client.get(reverse("chat:chat_room", args=[12]))

        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('chat:chat_room', args=[12])}"
        )

    def test_room_is_created_and_user_joins(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("chat:chat_room", args=[12]))

        room = ChatRoom.objects.get(pk=12)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(room.name, "Chat Room 12")
        self.assertTrue(room.users.filter(pk=self.user.pk).exists())
        self.assertEqual(response.context["chat_room"], room)

    def test_room_shows_the_five_most_recent_messages_in_order(self):
        self.client.force_login(self.user)
        room = ChatRoom.objects.create(name="General")
        messages = [
            Message.objects.create(user=self.user, chat_room=room, content=str(index))
            for index in range(7)
        ]

        response = self.client.get(reverse("chat:chat_room", args=[room.pk]))

        self.assertEqual(list(response.context["latest_messages"]), messages[-5:])
