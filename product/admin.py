from django.contrib import admin

from .models import ProductFavourite, Product, ProductImage, ProductColor, ProductSize, Variation, ProductReview


class ProductFavouriteAdmin(admin.TabularInline):
    """
    Display the product favourite model as a tabular inline.
    """
    model = ProductFavourite


class ProductAdmin(admin.ModelAdmin):
    """
    Customize the Products admin display.
    """
    inlines       = [ProductFavouriteAdmin] 
    
    class Meta:
        model = Product

# models admin site registeration
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(Variation)
admin.site.register(ProductReview)