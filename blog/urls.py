from django.urls import path

from .views import PostDetailView, PostListView, PostShareView

app_name = "blog"
urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
    path("<int:post_id>/share/", PostShareView.as_view(), name="post_share"),
]
