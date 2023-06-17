from django.db import models
from config.mixins import UserTimeStampMixin
from authentication.models import CustomUser
from authentication.strings import SET_HELP_SUPPORT_STATUS


# Create your models here.
class ExpenseName(UserTimeStampMixin):
    name = models.CharField(max_length=255, blank=False, null=False)


class HelpSupport(UserTimeStampMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    problems = models.TextField(max_length=500, blank=False, null=False)
    status = models.CharField(max_length=3, blank=True, null=False, choices=SET_HELP_SUPPORT_STATUS, default='UN')

    def __str__(self):
        return f'{self.user.get_full_name()}-{self.user.phone}-{self.status}'
