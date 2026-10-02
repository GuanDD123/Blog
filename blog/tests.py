from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Comment, Post


class PostModelTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="author", password="test-pass-123"
        )

    def test_save_generates_slug_and_published_manager_filters_drafts(self):
        published = Post.objects.create(
            author=self.author,
            title="A Test Post",
            content="Published content",
            status=Post.Status.PUBLISHED,
        )
        Post.objects.create(
            author=self.author,
            title="A Draft Post",
            content="Draft content",
            status=Post.Status.DRAFT,
        )

        self.assertEqual(published.slug, "a-test-post")
        self.assertQuerySetEqual(Post.published.all(), [published])
        self.assertEqual(
            published.get_absolute_url(),
            reverse(
                "blog:post_detail",
                kwargs={
                    "year": published.published_at.year,
                    "month": published.published_at.month,
                    "day": published.published_at.day,
                    "slug": published.slug,
                },
            ),
        )


class PostViewTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="author", password="test-pass-123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="reader", password="test-pass-123"
        )
        self.published = Post.objects.create(
            author=self.author,
            title="Published story",
            content="Visible content",
            published_at=timezone.now(),
            status=Post.Status.PUBLISHED,
        )
        self.draft = Post.objects.create(
            author=self.author,
            title="Private draft",
            content="Not public",
            status=Post.Status.DRAFT,
        )

    def test_post_list_displays_only_published_posts(self):
        response = self.client.get(reverse("blog:post_list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["posts"], [self.published])

    def test_detail_shows_only_active_comments(self):
        active_comment = Comment.objects.create(
            post=self.published, user=self.other_user, content="Visible comment"
        )
        Comment.objects.create(
            post=self.published,
            user=self.other_user,
            content="Hidden comment",
            active=False,
        )

        response = self.client.get(self.published.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["comments"], [active_comment])

    def test_only_post_author_can_edit_post(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("blog:post_edit", kwargs={"pk": self.published.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_draft_is_not_available_at_public_detail_url(self):
        response = self.client.get(self.draft.get_absolute_url())

        self.assertEqual(response.status_code, 404)
