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
    original_selling_price = models.FloatField(blank=False, null=False, default=0.0)
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
        return self.quantity * self.original_selling_price

    def save(self, *args, **kwargs):
        # Store the original selling prices when saving the voucher
        self.original_selling_price = self.product.dealer_selling_price
        super().save(*args, **kwargs)


class DSRSellingVoucher(UserTimeStampMixin):
    date = models.DateField(auto_now=True)
    product = models.ForeignKey(DSRProductWallet, on_delete=models.PROTECT)
    sold_quantity = models.IntegerField(blank=False, null=False, default=0)
    returned_product = models.IntegerField(blank=False, null=False)
    damage_product = models.IntegerField(blank=False, null=False)
    original_selling_price = models.FloatField(blank=False, null=False, default=0.0)
    dsr = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_delivery_sales_representative": True},
        blank=False,
        null=False,
        related_name="dsr_selling_voucher",
    )

    @property
    def get_sold_price(self):
        return self.sold_quantity * self.original_selling_price

    def __str__(self):
        return f"{self.date}->{self.product}->{self.returned_product}->{self.damage_product}->{self.dsr.get_full_name()}"

    def save(self, *args, **kwargs):
        # Store the original selling prices when saving the voucher
        self.original_selling_price = self.product.dsr_product.dealer_selling_price
        super().save(*args, **kwargs)


class DSRSales(UserTimeStampMixin):
    date = models.DateField(auto_now=True)
    dsr = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_delivery_sales_representative": True},
        blank=False,
        null=False,
        related_name="dsr_sales",
    )
    total_selling_price = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    @property
    def get_payable_amount(self):
        return self.total_selling_price - self.discount

    @property
    def get_due_amount(self):
        return self.get_payable_amount - self.paid_amount

    def __str__(self):
        return f"{self.date}->{self.get_due_amount}"

    class Meta:
        verbose_name = "DSR Sale"
        verbose_name_plural = "DSR Sales"


class DSRCollections(UserTimeStampMixin):
    date = models.DateField(auto_now=True)
    dsr = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_delivery_sales_representative": True},
        blank=False,
        null=False,
        related_name="dsr_collection",
    )
    collected_amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.date}->{self.collected_amount}"

    class Meta:
        verbose_name = "DSR Collection"
        verbose_name_plural = "DSR Collections"
