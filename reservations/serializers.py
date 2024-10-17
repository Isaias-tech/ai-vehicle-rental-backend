from rest_framework import serializers
from .models import Reservation, Transaction
from vehicles.models import VehicleDetails
from vehicles.serializers import VehicleDetailsSerializer


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "user", "vehicle", "start_date", "end_date", "is_active", "is_canceled"]

    def get_vehicle_details(self, obj):
        vehicle_details = VehicleDetails.objects.get(vehicle=obj.vehicle)
        return VehicleDetailsSerializer(vehicle_details).data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "reservation", "braintree_transaction_id", "amount", "status", "created_at"]

    def get_vehicle_details(self, obj):
        vehicle_details = VehicleDetails.objects.get(vehicle=obj.reservation.vehicle)
        return VehicleDetailsSerializer(vehicle_details).data
