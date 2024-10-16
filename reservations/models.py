from django.db import models
from django.conf import settings
from vehicles.models import Vehicle


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reserved_from = models.DateTimeField()
    reserved_until = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="pending",
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation by {self.user} for {self.vehicle} from {self.reserved_from} to {self.reserved_until}"


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[("credit_card", "Credit Card"), ("paypal", "PayPal")])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")],
        default="pending",
    )
    transaction_date = models.DateTimeField(auto_now_add=True)

    # Braintree-specific fields
    braintree_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    braintree_status = models.CharField(max_length=255, null=True, blank=True)
    braintree_error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Transaction for {self.reservation} with status {self.status}"
