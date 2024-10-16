# Generated by Django 5.1.1 on 2024-10-16 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0004_alter_vehiclebrand_name_alter_vehiclemodel_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="image1",
            field=models.ImageField(blank=True, null=True, upload_to="vehicle_images/"),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="image2",
            field=models.ImageField(blank=True, null=True, upload_to="vehicle_images/"),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="image3",
            field=models.ImageField(blank=True, null=True, upload_to="vehicle_images/"),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="image4",
            field=models.ImageField(blank=True, null=True, upload_to="vehicle_images/"),
        ),
    ]
