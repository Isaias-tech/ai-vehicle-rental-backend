from .models import Vehicle, VehicleDetails
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "name",
            "make",
            "model",
            "year",
            "is_available",
            "price",
            "price_per_day",
            "price_per_week",
            "price_per_month",
            "picture1",
            "picture2",
            "picture3",
            "picture4",
            "created_at",
            "updated_at",
        ]


class VehicleDetailsSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = VehicleDetails
        fields = [
            "vehicle",
            "mileage",
            "color",
            "is_new",
            "is_automatic",
            "has_air_conditioning",
            "description",
            "created_at",
            "updated_at",
        ]
