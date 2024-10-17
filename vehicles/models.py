from utils.image_renamer import wrapper
from django.db import models


class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    picture1 = models.ImageField(upload_to=wrapper)
    picture2 = models.ImageField(upload_to=wrapper, blank=True, null=True)
    picture3 = models.ImageField(upload_to=wrapper, blank=True, null=True)
    picture4 = models.ImageField(upload_to=wrapper, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} {self.price}"


class VehicleDetails(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=255)
    is_new = models.BooleanField(default=True)
    is_automatic = models.BooleanField(default=True)
    has_air_conditioning = models.BooleanField(default=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle.year} {self.vehicle.make} {self.vehicle.model}"
