import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from config.mixins import TimeStampMixin, UserTimeStampMixin
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password, **kwargs):
        if not phone:
            raise ValueError('Phone is required')

        email = self.normalize_email(phone)
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, phone, password, **kwargs):
        kwargs.setdefault('is_admin', True)
        return self._create_user(phone, password, **kwargs)

    def create_user(self, phone, password, **kwargs):
        kwargs.setdefault('is_user', True)
        return self._create_user(phone, password, **kwargs)

    def create_customer(self, phone, password, **kwargs):
        kwargs.setdefault('is_customer', True)
        return self._create_user(phone, password, **kwargs)

    def create_dealer(self, phone, password, **kwargs):
        kwargs.setdefault('is_dealer', True)
        return self._create_user(phone, password, **kwargs)

    def create_retailer(self, phone, password, **kwargs):
        kwargs.setdefault('is_retailer', True)
        return self._create_user(phone, password, **kwargs)

    def create_direct_retailer(self, phone, password, **kwargs):
        kwargs.setdefault('is_direct_retailer', True)
        return self._create_user(phone, password, **kwargs)

    def create_sales_representative(self, phone, password, **kwargs):
        kwargs.setdefault('is_sales_representative', True)
        return self._create_user(phone, password, **kwargs)

    def create_delivery_sales_representative(self, phone, password, **kwargs):
        kwargs.setdefault('is_delivery_sales_representative', True)
        return self._create_user(phone, password, **kwargs)

    def create_superuser(self, phone, password, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        kwargs.setdefault('is_user', True)
        kwargs.setdefault('is_customer', True)
        kwargs.setdefault('is_admin', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_dealer', True)
        kwargs.setdefault('is_retailer', True)
        kwargs.setdefault('is_direct_retailer', True)
        kwargs.setdefault('is_sales_representative', True)
        kwargs.setdefault('is_delivery_sales_representative', True)
        return self._create_user(phone, password, **kwargs)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneNumberField(unique=True, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    username = models.CharField(blank=True, null=True, max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=False)
    is_direct_retailer = models.BooleanField(default=False)
    is_sales_representative = models.BooleanField(default=False)
    is_delivery_sales_representative = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    EMAIL_FIELD = "phone"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name_plural = 'Users'


# class Customer(TimeStampMixin):
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.OneToOneField(CustomUser, on_delete=models.RESTRICT)
#     address = models.TextField()
#     phone_number = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.user

class UserInformation(UserTimeStampMixin):
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_address = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='user', null=True, blank=True, default='profile.png')
    shop_photo = models.ImageField(upload_to='user/shop', null=True, blank=True)
    nid_number = models.CharField(max_length=20, blank=True, null=True)
    trade_licence = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return f'{self.shop_name}-{self.user.get_full_name()}'
