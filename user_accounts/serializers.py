from rest_framework import serializers
from .models import UserAccount, Role, UserAccountDetails


class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False)

    class Meta:
        model = UserAccount
        fields = ["email", "first_name", "last_name", "password", "role"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["name"]


class UserAccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountDetails
        fields = [
            "profile_picture",
            "drivers_licence",
            "passport",
            "identity_card",
            "phone_number",
            "city",
            "address",
        ]
