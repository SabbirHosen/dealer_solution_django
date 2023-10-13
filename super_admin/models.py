from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from config.mixins import UserTimeStampMixin
from authentication.models import CustomUser
from authentication.strings import SET_HELP_SUPPORT_STATUS, SET_ROLE_CHOICES


# Create your models here.
class ExpenseName(UserTimeStampMixin):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class HelpSupport(UserTimeStampMixin):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=False, null=False
    )
    problems = models.TextField(max_length=500, blank=False, null=False)
    status = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        choices=SET_HELP_SUPPORT_STATUS,
        default="PR",
    )

    def __str__(self):
        return f"{self.user.get_full_name()}-{self.user.phone}-{self.status}"


class RequestNewUser(models.Model):
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    user_number = PhoneNumberField(blank=False, null=False)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=3, choices=SET_ROLE_CHOICES)
    division = models.CharField(max_length=125, blank=True, null=True)
    district = models.CharField(max_length=125, blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name}-{self.request_date}"


class Company(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    dealers = models.ManyToManyField(
        CustomUser,
        through="DealerCompany",
        related_name="dealer_companies",
        blank=True,
    )

    def __str__(self):
        return self.name


class DealerCompany(models.Model):
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("dealer", "company")

    def __str__(self):
        return f"{self.dealer}-{self.company}"
