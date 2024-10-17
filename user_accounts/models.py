from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.crypto import get_random_string
from utils.send_emails import send_email
from utils.image_renamer import wrapper
from django.conf import settings
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address.")
        if not kwargs.get("first_name") or not kwargs.get("last_name"):
            raise ValueError("Users must provide first and last names.")

        user = self.model(email=self.normalize_email(email), **kwargs)

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


class UserAccount(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("ADMINISTRATOR", "Administrator"),
        ("MANAGER", "Manager"),
        ("EMPLOYEE", "Employee"),
        ("CLIENT", "Client"),
    ]
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, choices=ROLES, default="CLIENT")
    email = models.EmailField(unique=True, max_length=500)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    confirmation_token = models.CharField(max_length=50, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

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
        self.is_verified = False
        self.confirmation_token = None
        self.email = self.email + "_deleted_" + get_random_string(10)
        self.save()

    def verify_account(self, token: str):
        if self.confirmation_token != token:
            raise ValueError("Invalid token.")
        self.is_verified = True
        self.confirmation_token = None
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="account_details")

    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=wrapper, blank=True, null=True)

    passport = models.ImageField(upload_to=wrapper, blank=True, null=True)
    drivers_license = models.ImageField(upload_to=wrapper, blank=True, null=True)
    national_id = models.ImageField(upload_to=wrapper, blank=True, null=True)

    phone_number = models.CharField(max_length=255, blank=True, null=True)

    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.email
