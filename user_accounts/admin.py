from .models import UserAccount, UserAccountDetails, Role
from django.contrib import admin

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserAccountDetails)
admin.site.register(Role)
