from django.db import models
from config.mixins import UserTimeStampMixin
from authentication.models import CustomUser
from super_admin.models import Company
from authentication.strings import UNIT_CHOICES

# Create your models here.
class Product(UserTimeStampMixin):
    name = models.CharField(max_length=255, blank=False, name=False)
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    factor = models.PositiveSmallIntegerField(blank=False, name=False)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="carton")
    dealer_buying_price = models.PositiveIntegerField(blank=False, name=False)
    dealer_selling_price = models.PositiveIntegerField(blank=False, name=False)

    def __str__(self):
        return f"{self.name}->{self.company}->{self.dealer}"


class Stock(UserTimeStampMixin):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    def get_total_selling_price(self):
        return self.quantity * self.product.dealer_selling_price

    def get_total_buying_price(self):
        return self.quantity * self.product.dealer_buying_price

    def get_quantity_by_format(self):
        return {
            self.product.unit: self.quantity // self.product.factor,
            "piece": self.quantity % self.product.factor,
        }


class Voucher(UserTimeStampMixin):
    date = models.DateField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.date}->{self.product}->{self.quantity}"
