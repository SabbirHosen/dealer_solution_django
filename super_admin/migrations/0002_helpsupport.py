# Generated by Django 4.2.1 on 2023-06-17 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("super_admin", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HelpSupport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("problems", models.TextField(max_length=500)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("UN", "Unprocessed"),
                            ("PR", "Processing"),
                            ("DN", "Done"),
                        ],
                        default="UN",
                        max_length=3,
                    ),
                ),
                (
                    "created_by",
                    django_userforeignkey.models.fields.UserForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_related",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]