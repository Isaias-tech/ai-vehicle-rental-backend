from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import views, status
from .models import UserAccount
from .serializers import (
    UserAccountSerializer,
    PasswordChangeSerializer,
    UserAccountUpdateSerializer,
    DeleteAccountConfirmSerializer,
)
import logging

logger = logging.getLogger(__name__) 


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                logger.error("No refresh token provided in logout request")
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.exception("Error during logout: %s", e)
            return Response({"detail": "Error during logout."}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {
                        "message": "User created successfully. Please check your email to verify your account.",
                        "user": UserAccountSerializer(user).data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                logger.exception("Error during user registration: %s", e)
                return Response(
                    {"detail": "Error during user registration."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logger.error("Invalid data for user registration: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountVerificationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            logger.error("Verification token missing in request")
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(UserAccount, confirmation_token=token)

        try:
            user.verify_account(token)
            return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.warning("Error during account verification: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error during account verification: %s", e)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordChangeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.exception("Error during password change: %s", e)
                return Response({"detail": "Error updating password."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error("Invalid password change data: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserAccountUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"message": "User details updated successfully.", "user": serializer.data},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                logger.exception("Error during user update: %s", e)
                return Response({"detail": "Error updating user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error("Invalid data for user update: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = UserAccountSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error fetching user profile: %s", e)
            return Response({"detail": "Error fetching user profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDataView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            if user.role:
                if user.role.name in ["employee", "manager", "administrator"]:
                    if user.role.name == "administrator":
                        users = UserAccount.objects.all()
                    else:
                        users = UserAccount.objects.filter(is_active=True)

                    serializer = UserAccountSerializer(users, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            logger.warning("Permission denied for user: %s", user.email)
            return Response(
                {"error": "You do not have permission to access this data."}, status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            logger.exception("Error fetching user data: %s", e)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteAccountRequestView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.generate_confirmation_token()
            user.send_delete_verification_email()
            return Response({"message": "Delete confirmation email sent."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error requesting account deletion: %s", e)
            return Response(
                {"detail": "Error during account deletion request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteAccountConfirmView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DeleteAccountConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = serializer.validated_data["token"]
                user = get_object_or_404(UserAccount, confirmation_token=token)
                user.soft_delete()
                return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.exception("Error during account deletion confirmation: %s", e)
                return Response(
                    {"error": "Error confirming account deletion."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logger.error("Invalid data for account deletion confirmation: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
