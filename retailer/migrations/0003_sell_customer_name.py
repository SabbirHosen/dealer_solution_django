# Generated by Django 4.2.1 on 2023-06-10 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "retailer",
            "0002_alter_cashcollection_retailer_alter_expense_retailer_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="sell",
            name="customer_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]