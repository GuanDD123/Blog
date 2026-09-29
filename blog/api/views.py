from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from taggit.models import Tag

from utils.pagination import StandardPagination
from utils.permissions import IsAdminOrIsAuthorOrReadOnly

from ..models import Post
from .serializers import PostDetailSerializer, PostSerializer


class PostListView(ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Post.published.all()

        if tag_slug := self.kwargs.get("tag_slug"):
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        else:
            self.tag = None

        return queryset


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    permission_classes = (IsAdminOrIsAuthorOrReadOnly,)

    def get_queryset(self):
        return Post.published.filter(
            published_at__year=self.kwargs["year"],
            published_at__month=self.kwargs["month"],
            published_at__day=self.kwargs["day"],
        )
