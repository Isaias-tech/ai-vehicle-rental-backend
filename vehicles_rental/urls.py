from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("vr_admin/", admin.site.urls),
    path("api/accounts/", include("user_accounts.urls")),
]
