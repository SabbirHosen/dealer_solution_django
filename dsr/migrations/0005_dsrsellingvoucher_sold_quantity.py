# Generated by Django 4.2.1 on 2023-12-21 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dsr", "0004_alter_dsrcollections_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="dsrsellingvoucher",
            name="sold_quantity",
            field=models.IntegerField(default=0),
        ),
    ]