from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    LogoutView,
    UserRegistrationView,
    AccountVerificationView,
    PasswordChangeView,
    UserAccountUpdateView,
    UserDataView,
    UserProfileView,
    DeleteAccountRequestView,
    DeleteAccountConfirmView,
)


urlpatterns = [
    # User login with JWT
    path("login/", TokenObtainPairView.as_view(), name="login_token"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh_token"),
    # Custom user logout by blacklisting tokens
    path("logout/", LogoutView.as_view(), name="logout"),
    # Register user
    path("register/", UserRegistrationView.as_view(), name="register"),
    # Verify email by confirmation token
    path("verify_email/", AccountVerificationView.as_view(), name="email_verification"),
    # Update user data exepting password
    path("update/", UserAccountUpdateView.as_view(), name="update_user"),
    # Reset user password (Old-password, New-password, Re-new-password)
    path("reset-password/", PasswordChangeView.as_view(), name="reset_password"),
    # User details based on permissions
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("users/", UserDataView.as_view(), name="users-data"),
    # Request user account deletion
    path("delete/request/", DeleteAccountRequestView.as_view(), name="delete-request"),
    # Confirm user account deletion by confirmation token
    path("delete/confirm/", DeleteAccountConfirmView.as_view(), name="delete-confirm"),
]
