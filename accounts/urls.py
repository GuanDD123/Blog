from django.urls import include, path

from .views import RegisterView, dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
]
