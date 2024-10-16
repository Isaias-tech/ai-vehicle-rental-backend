from django.urls import path
from . import views

urlpatterns = [
    path("brands/", views.get_vehicle_brands),
    path("brands/create/", views.create_vehicle_brand),
    path("brands/update/<int:brandId>/", views.update_vehicle_brand),
    path("brands/delete/<int:brandId>/", views.delete_vehicle_brand),
    path("models/", views.get_vehicle_models),
    path("models/create/", views.create_vehicle_model),
    path("models/update/<int:modelId>/", views.update_vehicle_model),
    path("models/delete/<int:modelId>/", views.delete_vehicle_model),
    path("", views.get_vehicles),
    path("create/", views.create_vehicle),
    path("update/<int:vehicleId>/", views.update_vehicle),
    path("delete/<int:vehicleId>/", views.delete_vehicle),
    path("pricing/", views.get_pricings),
    path("pricing/create/", views.create_pricing),
    path("pricing/update/<int:pricingId>/", views.update_pricing),
    path("pricing/delete/<int:pricingId>/", views.delete_pricing),
    path("reports/", views.get_vehicle_reports),
    path("reports/create/", views.create_vehicle_report),
    path("reports/update/<int:reportId>/", views.update_vehicle_report),
    path("reports/delete/<int:reportId>/", views.delete_vehicle_report),
]
