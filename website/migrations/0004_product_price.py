# Generated by Django 4.2.2 on 2023-06-21 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_customer_address_customer_phone_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
