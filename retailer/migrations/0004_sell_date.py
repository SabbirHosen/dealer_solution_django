# Generated by Django 4.2.1 on 2023-06-12 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailer', '0003_sell_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sell',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]