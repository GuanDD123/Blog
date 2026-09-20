from django.urls import path

from .feeds import LatestPostsFeed
from .views import (
    PostCommentView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostSearch,
    PostSearchTrigramSimilarity,
    PostShareView,
    PostUpdateView,
)

app_name = "blog"
urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", PostListView.as_view(), name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
    path("new/", PostCreateView.as_view(), name="post_new"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("<int:pk>/share/", PostShareView.as_view(), name="post_share"),
    path("<int:pk>/comment/", PostCommentView.as_view(), name="post_comment"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", PostSearch.as_view(), name="post_search"),
    path(
        "search/trigram/",
        PostSearchTrigramSimilarity.as_view(),
        name="post_search_trigram",
    ),
]
