from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("user/", views.get_user, name="get_user"),
    path("users/", views.list_users, name="get_users"),
    path("users/update/<int:user_id>/", views.update_user_by_id, name="update_users"),
    path("users/delete/<int:user_id>/", views.delete_user_by_id, name="delete_users"),
    path("user/update/", views.update_user, name="update_user"),
    path("user/delete/", views.delete_user, name="delete_user"),
    path("user/delete/<int:user_id>/", views.delete_user_by_id, name="delete_user"),
    path("user/profile/", views.get_user_profile, name="get_profile"),
    path("user/profile/update/", views.update_user_profile, name="update_profile"),
]
