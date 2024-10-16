# Generated by Django 5.1.1 on 2024-10-16 13:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "group",
                    models.OneToOneField(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="auth.group"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("email", models.EmailField(max_length=500, unique=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("confirmation_token", models.CharField(blank=True, max_length=50, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="user_accounts.role"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserAccountDetails",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("profile_picture", models.ImageField(blank=True, null=True, upload_to="profile_pictures/%Y/%m/%d/")),
                ("drivers_licence", models.ImageField(blank=True, null=True, upload_to="drivers_licence/%Y/%m/%d/")),
                ("passport", models.ImageField(blank=True, null=True, upload_to="passport/%Y/%m/%d/")),
                ("identity_card", models.ImageField(blank=True, null=True, upload_to="identity_card/%Y/%m/%d/")),
                ("phone_number", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
