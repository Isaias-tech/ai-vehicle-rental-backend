from rest_framework.decorators import api_view, permission_classes
from reservations.serializers import ReservationSerializer, TransactionSerializer
from vehicles.serializers import VehicleDetailsSerializer
from utils.braintree_utils import get_braintree_gateway
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Reservation, Transaction
from vehicles.models import VehicleDetails
from django.db.models import Count, Sum
from vehicles.models import Vehicle
from rest_framework import status
from django.utils import timezone
from datetime import datetime


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    user = request.user
    vehicle_id = request.data.get("vehicle_id")
    start_date_str = request.data.get("start_date")
    end_date_str = request.data.get("end_date")
    amount = request.data.get("amount")
    payment_method_nonce = request.data.get("payment_method_nonce")

    try:
        # Parse the dates in MM/DD/YYYY format
        start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
        end_date = datetime.strptime(end_date_str, "%m/%d/%Y")

        # Make start_date and end_date timezone-aware (using the current timezone)
        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        vehicle = Vehicle.objects.get(id=vehicle_id)
        if not vehicle.is_available:
            return Response({"error": "Vehicle is not available."}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() >= start_date:
            return Response({"error": "Start date must be in the future."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date >= end_date:
            return Response({"error": "End date must be after the start date."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the reservation
        reservation = Reservation.objects.create(
            user=user, vehicle=vehicle, start_date=start_date, end_date=end_date, is_active=True
        )

        # Process payment through Braintree
        gateway = get_braintree_gateway()
        result = gateway.transaction.sale(
            {
                "amount": str(amount),
                "payment_method_nonce": payment_method_nonce,
                "options": {"submit_for_settlement": True},
            }
        )

        if result.is_success:
            # Save transaction details
            Transaction.objects.create(
                reservation=reservation,
                braintree_transaction_id=result.transaction.id,
                amount=result.transaction.amount,
                status=result.transaction.status,
            )

            # Mark the vehicle as unavailable
            vehicle.is_available = False
            vehicle.save()

            return Response({"message": "Reservation and payment successful!"}, status=status.HTTP_201_CREATED)
        else:
            # Delete the reservation if payment fails
            reservation.delete()
            return Response({"error": result.message}, status=status.HTTP_400_BAD_REQUEST)

    except Vehicle.DoesNotExist:
        return Response({"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"error": f"Invalid date format: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_reservation(request, reservation_id):
    user = request.user

    try:
        reservation = Reservation.objects.get(id=reservation_id, user=user)

        if reservation.is_canceled:
            return Response({"error": "Reservation is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

        reservation.cancel_reservation()

        return Response({"message": "Reservation canceled successfully."}, status=status.HTTP_200_OK)

    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_reservations(request):
    # Optional filters
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    s = request.query_params.get("status")

    # Build the queryset
    if request.user.role == "ADMINISTRATOR" or request.user.role == "MANAGER":
        queryset = Reservation.objects.all()
    else:
        queryset = Reservation.objects.filter(user=request.user)

    if start_date:
        queryset = queryset.filter(start_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(end_date__lte=end_date)
    if s:
        if s.lower() == "active":
            queryset = queryset.filter(is_active=True, is_canceled=False)
        elif s.lower() == "canceled":
            queryset = queryset.filter(is_canceled=True)

    # Serialize and return the data
    serializer = ReservationSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_transactions(request):
    # Optional filters
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    # Build the queryset
    queryset = Transaction.objects.all()

    if start_date:
        queryset = queryset.filter(reservation__start_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(reservation__end_date__lte=end_date)

    # Serialize and return the data
    serializer = TransactionSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_report(request):
    # Optional filters
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    # Filter reservations by date range if provided
    reservations = Reservation.objects.all()
    if start_date:
        reservations = reservations.filter(start_date__gte=start_date)
    if end_date:
        reservations = reservations.filter(end_date__lte=end_date)

    # 1. Most Requested Cars (Top 3)
    top_cars = (
        reservations.values("vehicle__id", "vehicle__name")
        .annotate(request_count=Count("vehicle"))
        .order_by("-request_count")[:3]
    )

    # 2. Attach Vehicle Details (Mileage, Description)
    top_cars_with_details = []
    for car in top_cars:
        vehicle_id = car["vehicle__id"]
        try:
            vehicle_details = VehicleDetails.objects.get(vehicle_id=vehicle_id)
            vehicle_data = {
                "vehicle_name": car["vehicle__name"],
                "request_count": car["request_count"],
                "vehicle_details": VehicleDetailsSerializer(vehicle_details).data,
            }
            top_cars_with_details.append(vehicle_data)
        except VehicleDetails.DoesNotExist:
            # If no vehicle details are found, append car data without it
            vehicle_data = {
                "vehicle_name": car["vehicle__name"],
                "request_count": car["request_count"],
                "vehicle_details": "No details available",
            }
            top_cars_with_details.append(vehicle_data)

    # 3. Total Income
    transactions = Transaction.objects.filter(reservation__in=reservations)
    total_income = transactions.aggregate(total_income=Sum("amount"))["total_income"] or 0

    # Build the report data
    report_data = {
        "most_requested_cars": top_cars_with_details,
        "total_income": total_income,
    }

    return Response(report_data, status=status.HTTP_200_OK)
