from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Product
from .utils import unique_slug_generator

@receiver(pre_save, sender=Product)     # receiver(signal, **kwargs) # to register a signal
def create_product_slug(sender, instance, *args, **kwargs):
    """
    Create a slug for a product before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)