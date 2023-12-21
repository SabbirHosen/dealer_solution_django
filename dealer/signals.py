from django.dispatch import receiver
from django.db.models.signals import pre_save
from dealer.models import DealerRepresentative
from authentication.models import CustomUser


@receiver(pre_save, sender=DealerRepresentative)
def update_representative_is_active(sender, instance, **kwargs):
    if instance:

        if instance.status == "activated":
            instance.representative.is_active = True
            instance.representative.save()
        else:
            instance.representative.is_active = False
            instance.representative.save()
