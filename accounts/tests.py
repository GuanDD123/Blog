from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from actions.models import Action

from .forms import UserRegistrationForm
from .models import Contact, Profile

User = get_user_model()


class AccountModelTests(TestCase):
    def test_user_and_profile_string_representations(self):
        user = User.objects.create_user(username="morgan", password="test-pass-123")
        profile = Profile.objects.create(user=user)

        self.assertEqual(str(user), "morgan")
        self.assertEqual(str(profile), "morgan's profile")
        self.assertEqual(
            user.get_absolute_url(), reverse("user_detail", args=[user.pk])
        )


class AccountFormTests(TestCase):
    def test_registration_rejects_an_existing_email(self):
        User.objects.create_user(
            username="existing", email="person@example.com", password="test-pass-123"
        )

        form = UserRegistrationForm(
            data={
                "username": "another",
                "email": "person@example.com",
                "password1": "A-strong-password-123",
                "password2": "A-strong-password-123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class UserFollowViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="follower", password="test-pass-123"
        )
        self.followed = User.objects.create_user(
            username="followed", password="test-pass-123"
        )
        self.client.force_login(self.user)

    def test_follow_and_unfollow_user(self):
        url = reverse("user_follow")

        response = self.client.post(url, {"pk": self.followed.pk, "action": "follow"})

        self.assertEqual(response.json(), {"status": "ok"})
        self.assertTrue(self.user.following.filter(pk=self.followed.pk).exists())
        self.assertTrue(
            Contact.objects.filter(user_from=self.user, user_to=self.followed).exists()
        )
        self.assertEqual(Action.objects.filter(user=self.user).count(), 1)

        response = self.client.post(url, {"pk": self.followed.pk, "action": "unfollow"})

        self.assertEqual(response.json(), {"status": "ok"})
        self.assertFalse(self.user.following.filter(pk=self.followed.pk).exists())
        self.assertFalse(
            Contact.objects.filter(user_from=self.user, user_to=self.followed).exists()
        )

    def test_follow_rejects_missing_fields_and_unknown_action(self):
        url = reverse("user_follow")

        self.assertEqual(self.client.post(url).json(), {"status": "error"})
        self.assertEqual(
            self.client.post(
                url, {"pk": self.followed.pk, "action": "subscribe"}
            ).json(),
            {"status": "error"},
        )


class RegistrationViewTests(TestCase):
    @patch("accounts.views.user_registed.delay")
    def test_registration_creates_profile_action_and_queues_email(self, queue_email):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-member",
                "email": "new@example.com",
                "password1": "A-strong-password-123",
                "password2": "A-strong-password-123",
            },
        )

        user = User.objects.get(username="new-member")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertTrue(
            Action.objects.filter(user=user, verb="created account").exists()
        )
        queue_email.assert_called_once_with(user.pk)
