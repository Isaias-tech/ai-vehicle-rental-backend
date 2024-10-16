from .serializers import UserAccountSerializer, UserAccountDetailsSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import UserAccount, UserAccountDetails, Role
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework import permissions
from django.db import transaction
from rest_framework import status


@transaction.atomic
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def create_user_account(request):
    data = request.data
    serialized = UserAccountSerializer(data=data)
    serialized.is_valid(raise_exception=True)

    try:
        role = Role.objects.filter(name=serialized.validated_data.pop("role")).first()
        if not role:
            role = Role.objects.get(name="Client")

        user: UserAccount = UserAccount.objects.create_user(**serialized.validated_data)
        user.role = role
        user.save()

        userDetails = UserAccountDetails(user=user)
        userDetails.save()

        user.send_verification_email()

        return Response({"message": "User account created!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_accounts(request):
    try:
        user: UserAccount = request.user

        if user.groups.filter(name="Client").exists():
            return Response(
                {"message": "Forbidden: Clients do not have access to this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )

        employee_group = Group.objects.get(name="Employee")
        client_group = Group.objects.get(name="Client")

        if user.groups.filter(name="Admin").exists():
            users = UserAccount.objects.all()
        elif user.groups.filter(name="Manager").exists():
            users = UserAccount.objects.filter(role__group__in=[employee_group, client_group])
        elif user.groups.filter(name="Employee").exists():
            users = UserAccount.objects.filter(role__group=client_group)
        else:
            users = []

        return Response([UserAccountSerializer(u).data for u in users])
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_logged_in_user(request):
    try:
        user: UserAccount = request.user
        return Response(UserAccountSerializer(user).data)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def log_out_user(request):
    try:
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"message": "Refresh token is required!"})

        refresh = RefreshToken(refresh)
        refresh.blacklist()

        return Response({"message": "User logged out!"})
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@transaction.atomic
@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_user_account(request):
    data = request.data
    user = request.user
    serialized = UserAccountSerializer(user, data=data, partial=True)
    serialized.is_valid(raise_exception=True)
    try:
        serialized.save()
        return Response(serialized.data)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_user_account(request):
    try:
        user: UserAccount = request.user
        user.generate_confirmation_token()
        user.send_delete_verification_email()
        return Response({"message": "User account confirmation email was sent!"})
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def delete_user_account_confirm(request, token):
    try:
        if not token:
            return Response({"message": "Token is required!"})
        if not UserAccount.objects.filter(confirmation_token=token).exists():
            return Response({"message": "Invalid token!"})

        user = UserAccount.objects.get(confirmation_token=token)
        user.soft_delete()

        return Response({"message": "User account deleted!"})
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    try:
        user: UserAccount = request.user
        profile = UserAccountDetails.objects.get(user=user)
        if not profile:
            return Response({"message": "User profile not found!"})
        return Response(UserAccountDetailsSerializer(profile).data)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@transaction.atomic
@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    user: UserAccount = request.user
    data = request.data
    profile = UserAccountDetails.objects.get(user=user)
    serialized = UserAccountDetailsSerializer(profile, data=data, partial=True)
    serialized.is_valid(raise_exception=True)
    try:
        serialized.save()
        return Response(serialized.data)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@transaction.atomic
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def reset_password(request):
    user: UserAccount = request.user
    data = request.data
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not old_password or not new_password:
        return Response({"message": "Old password and new password are required!"})
    if not user.check_password(old_password):
        return Response({"message": "Invalid old password!"})
    try:
        user.set_password(new_password)
        user.save()
        return Response({"message": "The password was reset!"})
    except Exception as e:
        return Response({"message": str(e)}, status=500)
