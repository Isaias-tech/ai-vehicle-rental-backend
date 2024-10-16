from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.crypto import get_random_string
from django.contrib.auth.models import Group
from utils.send_emails import send_email
from django.conf import settings
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address.")
        if not kwargs.get("first_name") or not kwargs.get("last_name"):
            raise ValueError("Users must provide first and last names.")

        user = self.model(email=self.normalize_email(email), **kwargs)

        user.generate_confirmation_token()
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password=password, **kwargs)

        user.is_superuser = True
        user.is_verified = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.group:
            group = Group.objects.create(name=self.name)
            self.group = group
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserAccount(AbstractBaseUser, PermissionsMixin):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    confirmation_token = models.CharField(max_length=50, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.role and self.role.group:
            self.groups.clear()
            self.groups.add(self.role.group)
        super(UserAccount, self).save(*args, **kwargs)

    def generate_confirmation_token(self):
        self.confirmation_token = get_random_string(length=50)
        self.save()

    def send_verification_email(self):
        user = self
        email_context = {
            "user": user,
            "confirmation_url": f"{settings.FRONTEND_URL}/confirm-account?token={user.confirmation_token}",
        }
        send_email("Account Confirmation", user, email_context, "account_verification")

    def send_delete_verification_email(self):
        user = self
        email_context = {
            "user": user,
            "confirmation_url": f"{settings.FRONTEND_URL}/delete-account?token={user.confirmation_token}",
        }
        send_email("Account Delete Confirmation", user, email_context, "delete_confirmation")

    def soft_delete(self):
        self.is_active = False
        self.confirmation_token = None
        self.email = self.email + "_deleted_" + get_random_string(10)
        self.save()

    def verify_account(self, token: str):
        if self.confirmation_token != token:
            raise ValueError("Invalid token.")
        self.is_verified = True
        self.confirmation_token = None
        self.save()


class UserAccountDetails(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="account_details")
    profile_picture = models.ImageField(upload_to="profile_pictures/%Y/%m/%d/", blank=True, null=True)

    drivers_licence = models.ImageField(upload_to="drivers_licence/%Y/%m/%d/", blank=True, null=True)
    passport = models.ImageField(upload_to="passport/%Y/%m/%d/", blank=True, null=True)
    identity_card = models.ImageField(upload_to="identity_card/%Y/%m/%d/", blank=True, null=True)

    phone_number = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.email
