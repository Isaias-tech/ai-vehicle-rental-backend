from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserAccountSerializer, UserProfileSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import UserProfile, UserAccount
from rest_framework import status
from django.db import transaction


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get("refresh")

    refresh_token = RefreshToken(refresh_token)
    refresh_token.blacklist()

    return Response(status=status.HTTP_200_OK)


@transaction.atomic
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    user: UserAccount = request.user
    data = request.data
    serializer = UserAccountSerializer(data=data)

    serializer.is_valid(raise_exception=True)

    if serializer.validated_data.get("role") == "ADMINISTRATOR" and user.role != "ADMINISTRATOR":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )
    elif serializer.validated_data.get("role") == "MANAGER" and user.role not in ["ADMINISTRATOR"]:
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )
    elif serializer.validated_data.get("role") == "EMPLOYEE" and user.role not in ["MANAGER", "ADMINISTRATOR"]:
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    serializer.save()

    profile = UserProfile(user=serializer.instance)
    profile.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserAccountSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_users(request):
    logged_in_user: UserAccount = request.user
    if logged_in_user.role == "CLIENT":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )
    if logged_in_user.role == "MANAGER":
        users = UserAccount.objects.filter(role__in=["CLIENT", "EMPLOYEE"], is_active=True)
    elif logged_in_user.role == "ADMINISTRATOR":
        users = UserAccount.objects.filter(is_active=True)
    elif logged_in_user.role == "EMPLOYEE":
        users = UserAccount.objects.filter(role="CLIENT", is_active=True)

    users = users.order_by("id")

    paginator = PageNumberPagination()
    paginated_vehicles = paginator.paginate_queryset(users, request)

    serializer = UserAccountSerializer(paginated_vehicles, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    serializer = UserAccountSerializer(user, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user_by_id(request, user_id: int):
    logged_in_user: UserAccount = request.user
    if logged_in_user.role != "ADMINISTRATOR" and logged_in_user.role != "MANAGER":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    if logged_in_user.role == "MANAGER":
        user = UserAccount.objects.filter(id=user_id, role__in=["CLIENT", "EMPLOYEE"]).first()
    else:
        user = UserAccount.objects.filter(id=user_id).first()

    data = request.data
    serializer = UserAccountSerializer(user, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user: UserAccount = request.user
    user.soft_delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_by_id(request, user_id: int):
    logged_in_user: UserAccount = request.user
    if logged_in_user.role != "ADMINISTRATOR" and logged_in_user.role != "MANAGER":
        return Response(
            {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
        )

    if logged_in_user.role == "MANAGER":
        user = UserAccount.objects.filter(id=user_id, role__in=["CLIENT", "EMPLOYEE"]).first()
    else:
        user = UserAccount.objects.filter(id=user_id).first()
    user.soft_delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return Response(UserProfileSerializer(profile).data, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    data = request.data

    serializer = UserProfileSerializer(profile, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
