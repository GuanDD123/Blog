from django.contrib.auth import get_user_model
from django.test import TestCase

from chat.models import ChatRoom

from .models import Action
from .utils import create_action


class CreateActionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="actor", password="test-pass-123"
        )
        self.room = ChatRoom.objects.create(name="General")

    def test_create_action_stores_generic_target(self):
        created = create_action(self.user, "joined room", self.room)

        action = Action.objects.get(user=self.user)
        self.assertTrue(created)
        self.assertEqual(action.verb, "joined room")
        self.assertEqual(action.target, self.room)

    def test_duplicate_action_for_same_target_is_suppressed(self):
        first_result = create_action(self.user, "joined room", self.room)
        second_result = create_action(self.user, "joined room", self.room)

        self.assertTrue(first_result)
        self.assertFalse(second_result)
        self.assertEqual(Action.objects.filter(user=self.user).count(), 1)

    def test_same_verb_for_another_target_is_recorded(self):
        another_room = ChatRoom.objects.create(name="Announcements")

        create_action(self.user, "joined room", self.room)
        created = create_action(self.user, "joined room", another_room)

        self.assertTrue(created)
        self.assertEqual(Action.objects.filter(user=self.user).count(), 2)
