from django.urls import path
from .views import (
    create_reservation,
    cancel_reservation,
    list_reservations,
    list_transactions,
    generate_report,
    get_braintree_token,
    top_frequent_clients,
)

urlpatterns = [
    path("create/", create_reservation, name="create_reservation"),
    path("cancel/<int:reservation_id>/", cancel_reservation, name="cancel_reservation"),
    path("list/", list_reservations, name="list_reservations"),
    path("transactions/", list_transactions, name="list_transactions"),
    path("report/", generate_report, name="generate_report"),
    path("braintree/get-client-token/", get_braintree_token, name="get_braintree_token"),
    path("top-frequent-clients/", top_frequent_clients, name="top_frequent_clients"),
]
