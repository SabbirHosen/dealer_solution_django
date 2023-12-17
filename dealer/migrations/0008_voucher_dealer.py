# Generated by Django 4.2.1 on 2023-12-17 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dealer", "0007_alter_voucher_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="voucher",
            name="dealer",
            field=models.ForeignKey(
                default=1,
                limit_choices_to={"is_dealer": True},
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="dealer_voucher",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
