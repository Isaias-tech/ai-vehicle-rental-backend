from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserAccountSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import UserProfile


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
