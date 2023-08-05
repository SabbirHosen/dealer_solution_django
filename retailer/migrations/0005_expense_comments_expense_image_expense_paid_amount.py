# Generated by Django 4.2.1 on 2023-06-12 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retailer", "0004_sell_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="comments",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="expense",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="retailer/expenses/comments"
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="paid_amount",
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
