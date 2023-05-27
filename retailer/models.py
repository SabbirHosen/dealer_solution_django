from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from config.mixins import TimeStampMixin, UserMixin, UserTimeStampMixin
from authentication.models import CustomUser
from super_admin.models import ExpenseName


# Create your models here.

class Sell(UserTimeStampMixin):
    payable_amount = models.IntegerField(blank=False, null=False)
    paid_amount = models.IntegerField(blank=False, null=False)
    customer_number = PhoneNumberField(blank=True, null=True)
    retailer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='retailer/sell', blank=True, null=True)

    @property
    def get_due(self):
        return self.payable_amount - self.paid_amount


class CashCollection(UserTimeStampMixin):
    paid_amount = models.IntegerField(blank=False, null=False)
    customer_number = PhoneNumberField(blank=False, null=False)
    retailer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)


class Expense(UserTimeStampMixin):
    retailer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    name = models.ForeignKey(ExpenseName, on_delete=models.CASCADE)
