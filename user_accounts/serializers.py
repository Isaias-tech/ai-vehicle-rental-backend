from rest_framework import serializers
from .models import UserAccount, UserProfile


class UserAccountSerializer(serializers.ModelSerializer):
    ROLES = [
        ("ADMINISTRATOR", "Administrator"),
        ("MANAGER", "Manager"),
        ("EMPLOYEE", "Employee"),
        ("CLIENT", "Client"),
    ]
    id = serializers.IntegerField(read_only=True)
    role = serializers.ChoiceField(choices=ROLES, default="CLIENT")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ["id", "role", "email", "first_name", "last_name", "password", "date_joined"]

    def create(self, validated_data):
        user_account = UserAccount.objects.create_user(**validated_data)
        user_account.set_password(validated_data["password"])
        user_account.save()
        return user_account


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "birth_date",
            "gender",
            "phone_number",
            "country",
            "city",
            "address",
            "profile_picture",
            "passport",
            "drivers_license",
            "national_id",
        ]
