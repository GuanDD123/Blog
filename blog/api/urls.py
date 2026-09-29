from django.urls import path

from .views import PostDetailView, PostListView

urlpatterns = [
    path("", PostListView.as_view()),
    path("tag/<slug:tag_slug>/", PostListView.as_view()),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", PostDetailView.as_view()),
]
