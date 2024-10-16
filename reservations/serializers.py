from rest_framework import serializers
from .models import Reservation, Transaction
from vehicles.models import Vehicle


class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.filter(is_deleted=False))
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "vehicle",
            "user",
            "reserved_from",
            "reserved_until",
            "status",
            "total_cost",
            "created_at",
            "updated_at",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    reservation = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.filter(is_deleted=False))
    braintree_transaction_id = serializers.ReadOnlyField()
    braintree_status = serializers.ReadOnlyField()
    braintree_error_message = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "reservation",
            "payment_method",
            "amount",
            "status",
            "transaction_date",
            "braintree_transaction_id",
            "braintree_status",
            "braintree_error_message",
        ]
