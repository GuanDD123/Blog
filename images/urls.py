from django.urls import path

from .views import ImageCreateView, ImageLikeView, ImageListView, image_detail

app_name = "images"
urlpatterns = [
    path("create/", ImageCreateView.as_view(), name="create"),
    path("detail/<int:pk>/<slug:slug>/", image_detail, name="detail"),
    path("like/", ImageLikeView.as_view(), name="like"),
    path("", ImageListView.as_view(), name="list"),
]
