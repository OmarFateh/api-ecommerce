from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Category
from product.utils import unique_slug_generator


@receiver(pre_save, sender=Category)     # receiver(signal, **kwargs) # to register a signal
def create_category_slug(sender, instance, *args, **kwargs):
    """
    Create a slug for a category before saving.
    """
    instance.slug = unique_slug_generator(instance) # assign slug to the instance
    parent_category_obj = instance.parent  # parent var
    while parent_category_obj is not None:
        instance.slug = f"{unique_slug_generator(parent_category_obj)}/{instance.slug}"
        parent_category_obj = parent_category_obj.parent