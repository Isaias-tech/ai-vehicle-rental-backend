from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_user_accounts, name="get_user_accounts"),
    path("user/", views.get_logged_in_user, name="get_logged_in_user"),
    path("register/", views.create_user_account, name="create_user_account"),
    path("login/", TokenObtainPairView.as_view(), name="login_token"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh_token"),
    path("logout/", views.log_out_user, name="log_out_user"),
    path("update/", views.update_user_account, name="update_user_account"),
    path("delete/", views.delete_user_account, name="delete_user_account"),
    path("delete/confirm/<str:token>/", views.delete_user_account_confirm, name="delete_user_account_confirm"),
    path("profile/", views.get_user_profile, name="get_user_profile"),
    path("profile/update/", views.update_user_profile, name="update_user_profile"),
    path("reset-password/", views.reset_password, name="reset_password"),
]
