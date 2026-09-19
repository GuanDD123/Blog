from django.urls import path

from .views import ImageCreateView, image_detail

app_name = "images"
urlpatterns = [
    path("create/", ImageCreateView.as_view(), name="create"),
    path("detail/<int:id>/<slug:slug>/", image_detail, name="detail"),
]
