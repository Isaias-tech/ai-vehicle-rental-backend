from django.db import models
from django.conf import settings
from vehicles.models import Vehicle


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def cancel_reservation(self):
        self.is_canceled = True
        self.is_active = False
        self.vehicle.is_available = True
        self.vehicle.save()
        self.save()

    def __str__(self):
        return f"Reservation for {self.vehicle} by {self.user} from {self.start_date} to {self.end_date}"


class Transaction(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="transaction")
    braintree_transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.braintree_transaction_id} for Reservation {self.reservation.id}"
