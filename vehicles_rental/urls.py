from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path("vr_admin/", admin.site.urls),
    path("api/accounts/", include("user_accounts.urls")),
]

urlpatterns += static(settings.MEDIA_URL)
