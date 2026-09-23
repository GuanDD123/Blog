from django.urls import path

from .views import (
    ImageCreateView,
    ImageDeleteView,
    ImageDetailView,
    ImageLikeView,
    ImageListView,
    ImageRankingView,
)

app_name = "images"
urlpatterns = [
    path("", ImageListView.as_view(), name="list"),
    path("detail/<int:pk>/<slug:slug>/", ImageDetailView.as_view(), name="detail"),
    path("ranking/", ImageRankingView.as_view(), name="ranking"),
    path("create/", ImageCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", ImageDeleteView.as_view(), name="delete"),
    path("like/", ImageLikeView.as_view(), name="like"),
]
