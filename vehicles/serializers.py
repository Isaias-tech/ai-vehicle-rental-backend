from . import models
from rest_framework import serializers


class VehicleBrandSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.VehicleBrand
        fields = ["id", "name", "created_at", "updated_at"]


class VehicleModelSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    brand = serializers.PrimaryKeyRelatedField(queryset=models.VehicleBrand.objects.filter(is_deleted=False))

    class Meta:
        model = models.VehicleModel
        fields = ["id", "name", "brand", "created_at", "updated_at"]


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.Vehicle
        fields = [
            "id",
            "name",
            "model",
            "year",
            "color",
            "price",
            "is_new",
            "available_from",
            "available_until",
            "image1",
            "image2",
            "image3",
            "image4",
            "created_at",
            "updated_at",
            "is_deleted",
        ]


class PricingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.Pricing
        fields = ["id", "vehicle", "daily_rate", "weekly_rate", "monthly_rate"]


class VehicleReportSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.VehicleReport
        fields = ["id", "vehicle", "mileage", "condition", "report_date"]
