from django.db import models
from config.mixins import UserTimeStampMixin


# Create your models here.
class ExpenseName(UserTimeStampMixin):
    name = models.CharField(max_length=255, blank=False, null=False)

