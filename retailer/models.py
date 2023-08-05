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
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    retailer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='retailer/sell', blank=True, null=True)

    @property
    def get_due(self):
        return self.payable_amount - self.paid_amount


class CashCollection(UserTimeStampMixin):
    paid_amount = models.IntegerField(blank=False, null=False)
    due_amount = models.IntegerField(blank=False, null=False)
    customer_number = PhoneNumberField(blank=False, null=False)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    retailer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.customer_name}->{self.customer_number}->{self.paid_amount}'


class Expense(UserTimeStampMixin):
    retailer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    name = models.ForeignKey(ExpenseName, on_delete=models.CASCADE)
    paid_amount = models.IntegerField()
    comments = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='retailer/expenses/comments', null=True, blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}  {self.retailer.get_full_name()}'

