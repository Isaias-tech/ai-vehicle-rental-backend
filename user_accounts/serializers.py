from .models import UserAccount, UserAccountDetails
from rest_framework import serializers


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    re_new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data["new_password"] != data["re_new_password"]:
            raise serializers.ValidationError("New password and Re-new password do not match.")
        return data

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class UserAccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountDetails
        fields = ["profile_picture", "drivers_licence", "passport", "identity_card", "phone_number", "city", "address"]


class UserAccountSerializer(serializers.ModelSerializer):
    account_details = UserAccountDetailsSerializer(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ["email", "first_name", "last_name", "password", "role", "account_details"]

    def create(self, validated_data):
        account_details_data = validated_data.pop("account_details", None)

        user = UserAccount.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data.get("role", None),
        )

        if account_details_data:
            UserAccountDetails.objects.create(user=user, **account_details_data)
        else:
            UserAccountDetails.objects.create(user=user)

        return user

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value


class UserAccountDetailsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountDetails
        fields = ["profile_picture", "drivers_licence", "passport", "identity_card", "phone_number", "city", "address"]


class UserAccountUpdateSerializer(serializers.ModelSerializer):
    account_details = UserAccountDetailsUpdateSerializer(required=False)

    class Meta:
        model = UserAccount
        fields = ["email", "first_name", "last_name", "role", "account_details"]
        read_only_fields = ["email"]

    def update(self, instance, validated_data):
        account_details_data = validated_data.pop("account_details", None)

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.role = validated_data.get("role", instance.role)
        instance.save()

        account_details = instance.account_details
        if account_details_data:
            for attr, value in account_details_data.items():
                setattr(account_details, attr, value)
            account_details.save()

        return instance


class DeleteAccountConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            user = UserAccount.objects.get(confirmation_token=value)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")
        return value
