from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Image


class ImageModelTests(TestCase):
    def test_save_generates_slug_from_title(self):
        user = get_user_model().objects.create_user(
            username="photographer", password="test-pass-123"
        )
        image = Image.objects.create(
            user=user,
            title="A Bright Morning",
            url="https://example.com/photo.jpg",
            image="images/photo.jpg",
        )

        self.assertEqual(image.slug, "a-bright-morning")
        self.assertEqual(
            image.get_absolute_url(),
            reverse("images:detail", kwargs={"pk": image.pk, "slug": image.slug}),
        )


class ImageLikeViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="liker", password="test-pass-123"
        )
        self.owner = get_user_model().objects.create_user(
            username="owner", password="test-pass-123"
        )
        self.image = Image.objects.create(
            user=self.owner,
            title="Sample photo",
            url="https://example.com/photo.jpg",
            image="images/photo.jpg",
        )
        self.url = reverse("images:like")
        self.client.force_login(self.user)

    def test_like_and_unlike_update_relationship_and_count(self):
        response = self.client.post(self.url, {"pk": self.image.pk, "action": "like"})

        self.image.refresh_from_db()
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertTrue(self.image.users_like.filter(pk=self.user.pk).exists())
        self.assertEqual(self.image.users_like_count, 1)

        response = self.client.post(self.url, {"pk": self.image.pk, "action": "unlike"})

        self.image.refresh_from_db()
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertFalse(self.image.users_like.filter(pk=self.user.pk).exists())
        self.assertEqual(self.image.users_like_count, 0)

    def test_like_rejects_missing_fields_and_unknown_action(self):
        self.assertEqual(self.client.post(self.url).json(), {"status": "error"})
        self.assertEqual(
            self.client.post(self.url, {"pk": self.image.pk, "action": "star"}).json(),
            {"status": "error"},
        )
