from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from authentication.models import CustomUser, UserInformation


@receiver(post_save, sender=CustomUser)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            UserInformation.objects.create(user=instance)
