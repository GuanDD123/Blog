from django.db.models import Count
from rest_framework import serializers

from ..models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "published_at", "tags")


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user", "post", "content", "created_at")


class PostDetailSerializer(PostSerializer):
    comments = serializers.SerializerMethodField()
    similar_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "published_at",
            "tags",
            "comments",
            "similar_posts",
        )

    def get_comments(self, obj):
        comments = obj.comments.filter(active=True)
        return CommentSerializer(comments, many=True).data

    def get_similar_posts(self, obj):
        similar_posts = (
            Post.published.filter(tags__in=obj.tags.values_list("pk", flat=True))
            .exclude(pk=obj.pk)
            .annotate(same_tags=Count("tags"))
            .order_by("-same_tags", "-published_at")[:3]
        )
        return PostSerializer(similar_posts, many=True).data
