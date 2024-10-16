from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_reservation),
    path("transactions/create/", views.create_transaction),
    path("invoices/", views.list_user_invoices),
    path("invoices/<int:user_id>/", views.search_user_reservations),
    path("reports/income/", views.period_income_report),
]
