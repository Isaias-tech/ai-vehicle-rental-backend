from django.forms import ValidationError
from django.utils.crypto import get_random_string
from django.db import models


class VehicleBrand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


def wrapper(instance, filename):
    ext = filename.split(".")[-1].lower()

    if ext not in ["jpg", "png", "jpeg"]:
        raise ValidationError(f"invalid image extension: {filename}")

    filename = f"vehicle_images/{get_random_string(50)}.{ext}"
    return filename


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    year = models.IntegerField()
    color = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_new = models.BooleanField(default=False)
    available_from = models.DateField(default=None)
    available_until = models.DateField(default=None)
    image1 = models.ImageField(upload_to=wrapper)
    image2 = models.ImageField(upload_to=wrapper, null=True, blank=True)
    image3 = models.ImageField(upload_to=wrapper, null=True, blank=True)
    image4 = models.ImageField(upload_to=wrapper, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.model.name})"


class Pricing(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Pricing for {self.vehicle.name}: {self.daily_rate} per day"


class VehicleReport(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mileage = models.IntegerField()
    condition = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for {self.vehicle.name} on {self.report_date}"
