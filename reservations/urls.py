from django.urls import path
from .views import create_reservation, cancel_reservation, list_reservations, list_transactions, generate_report

urlpatterns = [
    path("create/", create_reservation, name="create_reservation"),
    path("cancel/<int:reservation_id>/", cancel_reservation, name="cancel_reservation"),
    path("list/", list_reservations, name="list_reservations"),
    path("transactions/", list_transactions, name="list_transactions"),
    path("report/", generate_report, name="generate_report"),
]
