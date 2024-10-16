from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from user_accounts.models import UserAccount
from rest_framework import permissions
from rest_framework import status
from . import serializers, models


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_vehicle_brand(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = serializers.VehicleBrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_vehicle_brand(request, brandId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    brand = get_object_or_404(models.VehicleBrand, id=brandId)
    serializer = serializers.VehicleBrandSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_vehicle_brands(request):
    brandId = request.query_params.get("brandId", None)

    if brandId:
        brand = get_object_or_404(models.VehicleBrand, id=brandId)
        if brand.is_deleted:
            if not request.user.groups.filter(name__in=["Administrator", "Manager"]).exists():
                return Response(
                    {"error": "You do not have permission to access deleted items."}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = serializers.VehicleBrandSerializer(brand)
        return Response(serializer.data)

    brands = models.VehicleBrand.objects.filter(is_deleted=False)
    serializer = serializers.VehicleBrandSerializer(brands, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_vehicle_brand(request, brandId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    brand = get_object_or_404(models.VehicleBrand, id=brandId)
    brand.is_deleted = True
    brand.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_vehicle_model(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = serializers.VehicleModelSerializer(data=request.data)
    if serializer.is_valid():
        try:
            models.VehicleBrand.objects.get(id=request.data["brand"], is_deleted=False)
        except models.VehicleBrand.DoesNotExist:
            return Response(
                {"error": "The specified brand does not exist or has been deleted."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_vehicle_model(request, modelId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    model = get_object_or_404(models.VehicleModel, id=modelId)
    serializer = serializers.VehicleModelSerializer(model, data=request.data, partial=True)

    if serializer.is_valid():
        if "brand" in request.data:
            try:
                models.VehicleBrand.objects.get(id=request.data["brand"], is_deleted=False)
            except models.VehicleBrand.DoesNotExist:
                return Response(
                    {"error": "The specified brand does not exist or has been deleted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_vehicle_models(request):
    modelId = request.query_params.get("modelId", None)

    if modelId:
        res = get_object_or_404(models.VehicleModel, id=modelId)
        if res.is_deleted:
            if not request.user.groups.filter(name__in=["Administrator", "Manager"]).exists():
                return Response(
                    {"error": "You do not have permission to access deleted items."}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = serializers.VehicleModelSerializer(res)
        return Response(serializer.data)

    res = models.VehicleModel.objects.filter(is_deleted=False)
    serializer = serializers.VehicleModelSerializer(res, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_vehicle_model(request, modelId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    model = get_object_or_404(models.VehicleModel, id=modelId)
    model.is_deleted = True
    model.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_vehicle(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = serializers.VehicleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_vehicle(request, vehicleId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    vehicle = get_object_or_404(models.Vehicle, id=vehicleId)
    serializer = serializers.VehicleSerializer(vehicle, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_vehicles(request):
    vehicleId = request.query_params.get("vehicleId", None)

    if vehicleId:
        vehicle = get_object_or_404(models.Vehicle, id=vehicleId)
        if vehicle.is_deleted:
            if not request.user.groups.filter(name__in=["Administrator", "Manager"]).exists():
                return Response(
                    {"error": "You do not have permission to access deleted items."}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = serializers.VehicleSerializer(vehicle)
        return Response(serializer.data)

    vehicles = models.Vehicle.objects.filter(is_deleted=False)
    serializer = serializers.VehicleSerializer(vehicles, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_vehicle(request, vehicleId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    vehicle = get_object_or_404(models.Vehicle, id=vehicleId)
    vehicle.is_deleted = True
    vehicle.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_vehicle_availability(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = serializers.VehicleAvailabilitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_vehicle_availability(request, availabilityId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    availability = get_object_or_404(models.VehicleAvailability, id=availabilityId)
    serializer = serializers.VehicleAvailabilitySerializer(availability, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_vehicle_availabilities(request):
    availabilityId = request.query_params.get("availabilityId", None)

    if availabilityId:
        availability = get_object_or_404(models.VehicleAvailability, id=availabilityId)
        if availability.is_deleted:
            if not request.user.groups.filter(name__in=["Administrator", "Manager"]).exists():
                return Response(
                    {"error": "You do not have permission to access deleted items."}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = serializers.VehicleAvailabilitySerializer(availability)
        return Response(serializer.data)

    availabilities = models.VehicleAvailability.objects.filter(is_deleted=False)
    serializer = serializers.VehicleAvailabilitySerializer(availabilities, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_vehicle_availability(request, availabilityId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    availability = get_object_or_404(models.VehicleAvailability, id=availabilityId)
    availability.is_deleted = True
    availability.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_pricing(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = serializers.PricingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_pricing(request, pricingId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    pricing = get_object_or_404(models.Pricing, id=pricingId)
    serializer = serializers.PricingSerializer(pricing, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_pricings(request):
    pricingId = request.query_params.get("pricingId", None)

    if pricingId:
        pricing = get_object_or_404(models.Pricing, id=pricingId)
        if pricing.is_deleted:
            if not request.user.groups.filter(name__in=["Administrator", "Manager"]).exists():
                return Response(
                    {"error": "You do not have permission to access deleted items."}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = serializers.PricingSerializer(pricing)
        return Response(serializer.data)

    pricings = models.Pricing.objects.filter(is_deleted=False)
    serializer = serializers.PricingSerializer(pricings, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_pricing(request, pricingId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    pricing = get_object_or_404(models.Pricing, id=pricingId)
    pricing.is_deleted = True
    pricing.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_vehicle_report(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = serializers.VehicleReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_vehicle_report(request, reportId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    report = get_object_or_404(models.VehicleReport, id=reportId)
    serializer = serializers.VehicleReportSerializer(report, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_vehicle_reports(request):
    reportId = request.query_params.get("reportId", None)

    if reportId:
        report = get_object_or_404(models.VehicleReport, id=reportId)
        if report.is_deleted:
            if not request.user.groups.filter(name__in=["Administrator", "Manager"]).exists():
                return Response(
                    {"error": "You do not have permission to access deleted items."}, status=status.HTTP_403_FORBIDDEN
                )

        serializer = serializers.VehicleReportSerializer(report)
        return Response(serializer.data)

    reports = models.VehicleReport.objects.filter(is_deleted=False)
    serializer = serializers.VehicleReportSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_vehicle_report(request, reportId):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN
        )

    report = get_object_or_404(models.VehicleReport, id=reportId)
    report.is_deleted = True
    report.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
