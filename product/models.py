from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

def product_image(instance, filename):
    """
    Upload the product image into the path and return the uploaded image path.
    """   
    return f'products/{instance.variation.product.name}-{instance.variation.color.name}-{instance.variation.size.name}/{filename}'


class BaseTimestamp(models.Model):
    """
    Timestamp abstract model.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class ProductFavourite(BaseTimestamp):
    """
    A relationship model between the product and its favourites.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Product(BaseTimestamp):
    """
    Product model.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.CharField(max_length=255)
    details = models.TextField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    category = models.ForeignKey('category.Category', related_name="products", on_delete=models.SET_NULL, null=True)
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wishlist', blank=True, through=ProductFavourite)
    in_stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    # objects = ProductManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name.
        return f"{self.name}"

    @property
    def actual_price(self):
        # Return sale price if exists and if not, get regular price of product's variation 
        if self.sale_price:
            return self.sale_price
        else:
            return self.regular_price 

    def get_price_sale_difference(self):
        if self.sale_price:
            # Return the difference between regular price and sale price.
            return self.regular_price - self.sale_price

    def get_price_sale_difference_precentage(self):
        if self.sale_price:
            # Return the precentage difference between regular price and sale price.
            return (self.get_price_sale_difference()*100)// self.regular_price     

    # @property
    # def get_absolute_url(self):
    #     # Return absolute url of product detail by its slug.
    #     return reverse("product:product-detail", kwargs={"product_slug": self.slug})


class ProductImage(BaseTimestamp):
    """
    Product image model.
    """
    variation = models.ForeignKey('Variation', related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    # objects = ProductImageManager()

    class Meta:
        ordering = ['variation']

    def __str__(self):
        # Return variation.
        return f"{self.variation}"


class ProductColor(BaseTimestamp):
    """
    Product color model.
    """
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16)

    class Meta:
        ordering = ['name']

    def __str__(self):
        # Return color's name.
        return f"{self.name}"


class ProductSize(BaseTimestamp):
    """
    Product size model.
    """
    name = models.CharField(max_length=64)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # Return size's name.
        return f"{self.name}"


class Variation(BaseTimestamp):
    """
    Product variation model.
    """
    product = models.ForeignKey(Product, related_name="variations", on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, related_name="colors", on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, related_name="sizes", on_delete=models.CASCADE)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    # objects = VariationManager()

    class Meta:
        unique_together = ['product', 'color', 'size']
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name, color's name, and size's name.
        return f"{self.product.name} | {self.color.name} | {self.size.name}"

    @property
    def first_image(self):
        #  Return first image of a variation.
        return self.images.first()

    @property
    def actual_price(self):
        # Return sale price if exists and if not, get regular price of product's variation 
        if self.sale_price:
            return self.sale_price
        else:
            return self.regular_price        


class ProductReview(BaseTimestamp):
    """
    Product review model.
    """
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name, user's name and his rate.
        return f"{self.product.name} | {self.user.first_name} {self.user.last_name} | {self.rate} stars"

    def get_update_delete_absolute_url(self):
        # Return absolute url of update and delete review by its id.
        return reverse('accounts:update-delete-review', kwargs={'review_id': self.pk})

    def get_rate_precentage(self):
        # Return review rate precentage.
        return (self.rate * 20)