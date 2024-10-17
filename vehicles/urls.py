from .views import (
    create_vehicle,
    list_vehicles,
    update_vehicle,
    delete_vehicle,
    get_vehicle_details,
    update_vehicle_details,
)
from django.urls import path

urlpatterns = [
    path("create/", create_vehicle),
    path("list/", list_vehicles),
    path("update/<int:vehicle_id>/", update_vehicle),
    path("delete/<int:vehicle_id>/", delete_vehicle),
    path("details/<int:vehicle_id>/", get_vehicle_details),
    path("details/update/<int:vehicle_id>/", update_vehicle_details),
]
