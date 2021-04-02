from django.db import models
from django.urls import reverse

from product.models import BaseTimestamp

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel, BaseTimestamp):
    """
    Category model implemented with MPTT.
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'parent')
        verbose_name_plural = 'Categories'

    def __str__(self):
        # Return category's name
        return self.name

    def save(self, *args, **kwargs):
        # prevent a category to be itself parent.
        if self.id and self.parent and self.id == self.parent.id:
            self.parent = None
        super().save(*args, **kwargs)

    def get_parent(self):
        # Return category's parent. 
        if self.parent:
            return self.parent 
        else: 
            return self 

    # def get_absolute_url(self):
    #     # Return absolute url of category list by its slug.
    #     return reverse("category:category-list", kwargs={"category_slug": self.slug})
