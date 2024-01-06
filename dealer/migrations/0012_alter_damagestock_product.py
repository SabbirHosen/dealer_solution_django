# Generated by Django 4.2.1 on 2024-01-06 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dealer", "0011_damagestock_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="damagestock",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="damage_stock",
                to="dealer.product",
            ),
        ),
    ]
