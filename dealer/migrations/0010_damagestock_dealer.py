# Generated by Django 4.2.1 on 2023-12-21 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dealer", "0009_damagestock"),
    ]

    operations = [
        migrations.AddField(
            model_name="damagestock",
            name="dealer",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"is_dealer": True},
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="dealer_damage_product",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
