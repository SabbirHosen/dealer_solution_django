from django.db import models

from config.mixins import UserTimeStampMixin
from dealer.models import Product
from authentication.models import CustomUser


# Create your models here.
class DSRProductWallet(UserTimeStampMixin):
    dsr_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="dsr_product"
    )
    dsr = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="dsr_product_wallet",
        limit_choices_to={"is_delivery_sales_representative": True},
    )
    quantity = models.IntegerField(default=0)
    returned_quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.dsr_product.name + " - " + str(self.quantity))

    class Meta:
        unique_together = ("dsr_product", "dsr")


class DSRVoucher(UserTimeStampMixin):
    date = models.DateField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(blank=False, null=False)
    price = models.FloatField(blank=False, null=False, default=0)
    dsr = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_delivery_sales_representative": True},
        blank=False,
        null=False,
        related_name="dsr_voucher",
    )

    def __str__(self):
        return (
            f"{self.date}->{self.product}->{self.quantity}->{self.dsr.get_full_name()}"
        )

    def get_total_selling_price(self):
        return self.quantity * self.product.dealer_selling_price
