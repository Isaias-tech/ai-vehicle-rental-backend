from django.contrib import admin
from .models import Vehicle, VehicleBrand, VehicleModel, VehicleAvailability, Pricing, VehicleReport

admin.site.register(Vehicle)
admin.site.register(VehicleBrand)
admin.site.register(VehicleModel)
admin.site.register(VehicleAvailability)
admin.site.register(Pricing)
admin.site.register(VehicleReport)
