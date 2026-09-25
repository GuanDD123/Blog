from django.urls import include, path

from .views import (
    DashBoard,
    EditView,
    RegisterView,
    UserDetailView,
    UserFollowView,
    UserListView,
)

urlpatterns = [
    path("", DashBoard.as_view(), name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("edit/", EditView.as_view(), name="edit"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/follow/", UserFollowView.as_view(), name="user_follow"),
]
