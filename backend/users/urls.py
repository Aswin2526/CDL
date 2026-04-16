from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    LoginView,
    LogoutView,
    ProfileImageUploadView,
    ProfileView,
    RegisterView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/image/", ProfileImageUploadView.as_view(), name="profile_image"),
]
