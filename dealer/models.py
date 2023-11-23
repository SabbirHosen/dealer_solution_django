from django.db import models
from config.mixins import UserTimeStampMixin
from authentication.models import CustomUser
from super_admin.models import Company, ExpenseName
from authentication.strings import UNIT_CHOICES, DEALER_REPRESENTATIVE_STATUS

# Create your models here.
class Product(UserTimeStampMixin):
    name = models.CharField(max_length=255, blank=False, name=False)
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    factor = models.PositiveSmallIntegerField(blank=False, name=False)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="carton")
    dealer_buying_price = models.FloatField(blank=False, name=False)
    dealer_selling_price = models.FloatField(blank=False, name=False)

    def __str__(self):
        return f"{self.name}->{self.company}->{self.dealer}"


class Stock(UserTimeStampMixin):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.product}->{self.quantity}"

    def get_total_selling_price(self):
        return self.quantity * self.product.dealer_selling_price

    def get_total_buying_price(self):
        return self.quantity * self.product.dealer_buying_price

    def get_quantity_by_format(self):
        return {
            self.product.unit: self.quantity // self.product.factor,
            "piece": self.quantity % self.product.factor,
        }

    def get_quantity_in_unit(self):
        return self.quantity // self.product.factor

    def get_quantity_in_piece(self):
        return self.quantity % self.product.factor


class Voucher(UserTimeStampMixin):
    date = models.DateField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    price = models.FloatField(blank=False, null=False, default=0)

    def __str__(self):
        return f"{self.date}->{self.product}->{self.quantity}"

    def get_total_selling_price(self):
        return self.quantity * self.product.dealer_selling_price

    def get_total_buying_price(self):
        return self.quantity * self.product.dealer_buying_price

    @property
    def get_quantity_by_format(self):
        return {
            self.product.get_unit_display(): self.quantity // self.product.factor,
            "piece": self.quantity % self.product.factor,
        }


class DealerExpense(UserTimeStampMixin):
    dealer = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    name = models.ForeignKey(ExpenseName, on_delete=models.CASCADE)
    paid_amount = models.IntegerField()
    comments = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to="dealer/expenses/comments", null=True, blank=True
    )
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.dealer.get_full_name()}>>{self.date}"


class DealerRepresentative(UserTimeStampMixin):
    dealer = models.ForeignKey(
        CustomUser,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_dealer": True},
        blank=False,
        null=False,
        related_name="dealer_representative",
    )
    representative = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="representative_dealer",
        blank=False,
        null=False,
    )
    status = models.CharField(max_length=13, choices=DEALER_REPRESENTATIVE_STATUS)

    def save(self, *args, **kwargs):

        if (
            self.representative.is_sales_representative
            or self.representative.is_delivery_sales_representative
        ):
            super(DealerRepresentative, self).save(*args, **kwargs)
        else:

            raise ValueError(f"Only DSR or SR  are allowed for this relationship.")
