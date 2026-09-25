from django.urls import path

from .feeds import LatestPostsFeed
from .views import (
    PostCommentView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostSearchTrigramSimilarityView,
    PostSearchView,
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
    path("edit/<int:pk>/", PostUpdateView.as_view(), name="post_edit"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("share/<int:pk>/", PostShareView.as_view(), name="post_share"),
    path("comment/<int:pk>/", PostCommentView.as_view(), name="post_comment"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", PostSearchView.as_view(), name="post_search"),
    path(
        "search/trigram/",
        PostSearchTrigramSimilarityView.as_view(),
        name="post_search_trigram",
    ),
]
