from django.core.management.base import BaseCommand
from django.utils import timezone
from reservations.models import Reservation


class Command(BaseCommand):
    help = "Update vehicle availability based on reservation start and end dates"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Get all active reservations that have passed their end date
        expired_reservations = Reservation.objects.filter(end_date__lte=now, is_active=True)

        for reservation in expired_reservations:
            vehicle = reservation.vehicle
            vehicle.is_available = True  # Make the vehicle available again
            vehicle.save()

            # Mark the reservation as no longer active
            reservation.is_active = False
            reservation.save()

            self.stdout.write(
                self.style.SUCCESS(f"Updated reservation {reservation.id}: Vehicle {vehicle.name} is now available.")
            )

        # Check if there are any upcoming reservations and mark the vehicle unavailable
        upcoming_reservations = Reservation.objects.filter(start_date__lte=now, end_date__gte=now, is_active=True)

        for reservation in upcoming_reservations:
            vehicle = reservation.vehicle
            vehicle.is_available = False  # Make the vehicle unavailable
            vehicle.save()

            self.stdout.write(
                self.style.SUCCESS(f"Updated reservation {reservation.id}: Vehicle {vehicle.name} is now unavailable.")
            )

        self.stdout.write(self.style.SUCCESS("Vehicle status update complete."))
