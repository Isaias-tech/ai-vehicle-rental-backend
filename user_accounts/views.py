from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserAccountSerializer, UserProfileSerializer
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
    data = request.data
    serializer = UserAccountSerializer(data=data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    profile = UserProfile(user=serializer.instance)
    profile.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserAccountSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
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
