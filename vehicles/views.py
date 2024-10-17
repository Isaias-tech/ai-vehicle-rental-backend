from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import VehicleSerializer, VehicleDetailsSerializer
from rest_framework.response import Response
from .models import Vehicle, VehicleDetails
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db import transaction


@transaction.atomic
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_vehicle(request):
    user = request.user

    if user.role != "ADMINISTRATOR" and user.role != "MANAGER":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data
    serializer = VehicleSerializer(data=data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    VehicleDetails.objects.create(vehicle=serializer.instance)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_vehicles(request):
    name_contains = request.query_params.get("name_contains", None)

    vehicles = Vehicle.objects.filter(is_deleted=False)

    if name_contains:
        vehicles = vehicles.filter(name__icontains=name_contains)

    paginator = PageNumberPagination()
    paginated_vehicles = paginator.paginate_queryset(vehicles, request)

    serializer = VehicleSerializer(paginated_vehicles, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["PUT", "PATCH"])
@permission_classes([AllowAny])
def update_vehicle(request, vehicle_id):
    user = request.user
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()

    if user.role != "ADMINISTRATOR" and user.role != "MANAGER":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    if vehicle is None:
        return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = VehicleSerializer(instance=vehicle, data=data, partial=True)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_vehicle(request, vehicle_id):
    user = request.user
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()

    if user.role != "ADMINISTRATOR" and user.role != "MANAGER":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    if vehicle is None:
        return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

    vehicle.is_deleted = True
    vehicle.is_available = False
    vehicle.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_vehicle_details(request, vehicle_id):
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()

    if vehicle is None:
        return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

    vehicle_details = VehicleDetails.objects.filter(vehicle=vehicle).first()

    if vehicle_details is None:
        return Response({"error": "Vehicle details not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = VehicleDetailsSerializer(vehicle_details)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_vehicle_details(request, vehicle_id):
    user = request.user
    vehicle = Vehicle.objects.filter(id=vehicle_id).first()

    if user.role != "ADMINISTRATOR" and user.role != "MANAGER":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    if vehicle is None:
        return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

    vehicle_details = VehicleDetails.objects.filter(vehicle=vehicle).first()

    if vehicle_details is None:
        return Response({"error": "Vehicle details not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = VehicleDetailsSerializer(instance=vehicle_details, data=data, partial=True)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
