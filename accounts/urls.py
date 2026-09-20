from django.urls import include, path

from .views import EditView, RegisterView, UserDetailView, UserListView, dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("edit/", EditView.as_view(), name="edit"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
