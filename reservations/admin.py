from django.contrib import admin
from .models import Reservation, Transaction

# Register your models here.

admin.site.register(Reservation)
admin.site.register(Transaction)
