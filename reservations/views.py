from .serializers import ReservationSerializer, TransactionSerializer
from rest_framework.decorators import api_view, permission_classes
from user_accounts.models import UserAccount
from vehicles_rental.settings import gateway
from .models import Reservation, Transaction
from rest_framework.response import Response
from utils.send_emails import send_email
from django.db.models import Sum, Count
from rest_framework import permissions
from rest_framework import status
from datetime import datetime


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_transaction(request):
    user: UserAccount = request.user

    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        transaction = serializer.save()

        reservation = transaction.reservation
        if reservation.status == "confirmed":
            return Response(
                {"error": "This reservation has already been confirmed and paid for."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        braintree_result = gateway.transaction.sale(
            {
                "amount": str(transaction.amount),
                "payment_method_nonce": request.data.get("payment_method_nonce"),
                "options": {"submit_for_settlement": True},
            }
        )

        if braintree_result.is_success:
            transaction.braintree_transaction_id = braintree_result.transaction.id
            transaction.braintree_status = braintree_result.transaction.status
            transaction.status = "completed"
            transaction.save()

            reservation = transaction.reservation
            reservation.status = "confirmed"
            reservation.save()

            email_context = {
                "user": user,
                "transaction": {
                    "transaction_id": transaction.braintree_transaction_id,
                    "payment_method": transaction.payment_method,
                    "amount": transaction.amount,
                    "created_at": transaction.transaction_date,
                    "result_message": transaction.braintree_error_message or "Transaction successful",
                },
            }

            send_email(subject="Your Transaction Receipt", user=user, email_context=email_context, template="invoice")

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            transaction.braintree_status = "failed"
            transaction.braintree_error_message = braintree_result.message
            transaction.status = "failed"
            transaction.save()

            return Response(
                {"error": "Transaction failed", "message": braintree_result.message}, status=status.HTTP_400_BAD_REQUEST
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_reservation(request):
    user = request.user
    serializer = ReservationSerializer(data=request.data)

    if serializer.is_valid():
        reservation = serializer.save(user=user)

        vehicle = reservation.vehicle
        conflicting_reservations = Reservation.objects.filter(
            vehicle=vehicle,
            reserved_from__lt=reservation.reserved_until,
            reserved_until__gt=reservation.reserved_from,
            status="confirmed",
        )

        if conflicting_reservations.exists():
            return Response(
                {"error": "This vehicle is already reserved during the selected time period."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_user_invoices(request):
    user = request.user

    reservations = Reservation.objects.filter(user=user, status="confirmed")

    result = []

    for reservation in reservations:
        transactions = Transaction.objects.filter(reservation=reservation, status="completed")
        reservation_data = ReservationSerializer(reservation).data
        transaction_data = TransactionSerializer(transactions, many=True).data
        reservation_data["transactions"] = transaction_data
        result.append(reservation_data)

    return Response(result, status=200)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def search_user_reservations(request, user_id):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager", "Employee"]).exists():
        return Response({"error": "You do not have permission to perform this action."}, status=403)

    target_user = UserAccount.objects.get(id=user_id)

    reservations = Reservation.objects.filter(user=target_user)

    result = []

    for reservation in reservations:
        transactions = Transaction.objects.filter(reservation=reservation, status="completed")
        reservation_data = ReservationSerializer(reservation).data
        transaction_data = TransactionSerializer(transactions, many=True).data
        reservation_data["transactions"] = transaction_data
        result.append(reservation_data)

    return Response(result, status=200)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def period_income_report(request):
    user: UserAccount = request.user

    if not user.groups.filter(name__in=["Administrator", "Manager"]).exists():
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    start_date_str = request.query_params.get("start_date")
    end_date_str = request.query_params.get("end_date")

    if not start_date_str or not end_date_str:
        return Response({"error": "Please provide both start_date and end_date."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(
        transaction_date__gte=start_date, transaction_date__lte=end_date, status="completed"
    )

    total_income = transactions.aggregate(total=Sum("amount"))["total"] or 0.00

    most_requested_car = (
        Reservation.objects.filter(reserved_from__gte=start_date, reserved_until__lte=end_date, status="confirmed")
        .values("vehicle__name")
        .annotate(request_count=Count("vehicle"))
        .order_by("-request_count")
        .first()
    )

    most_requested_car_data = {
        "vehicle_name": most_requested_car["vehicle__name"] if most_requested_car else "N/A",
        "request_count": most_requested_car["request_count"] if most_requested_car else 0,
    }

    report_data = {
        "total_income": total_income,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "total_transactions": transactions.count(),
        "most_requested_car": most_requested_car_data,
    }

    return Response(report_data, status=status.HTTP_200_OK)
