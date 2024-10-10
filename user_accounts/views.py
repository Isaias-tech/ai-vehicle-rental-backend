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


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Error during logout."}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully. Please check your email to verify your account.",
                    "user": UserAccountSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountVerificationView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(UserAccount, confirmation_token=token)

        try:
            user.verify_account(token)
            return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserAccountUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User details updated successfully.", "user": serializer.data}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserAccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDataView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role:
            if user.role.name in ["employee", "manager", "administrator"]:
                if user.role.name == "administrator":
                    users = UserAccount.objects.all()
                else:
                    users = UserAccount.objects.filter(is_active=True)

                serializer = UserAccountSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "You do not have permission to access this data."}, status=status.HTTP_403_FORBIDDEN)


class DeleteAccountRequestView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.generate_confirmation_token()
        user.send_delete_verification_email()
        return Response({"message": "Delete confirmation email sent."}, status=status.HTTP_200_OK)


class DeleteAccountConfirmView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DeleteAccountConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]
            user = get_object_or_404(UserAccount, confirmation_token=token)

            user.soft_delete()
            return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
