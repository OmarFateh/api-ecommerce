from django.db import models
from django.conf import settings

from product.models import BaseTimestamp


class OrderManager(models.Manager):
    """
    Order manager model.
    """
    def paid_orders(self):
        """
        """
        return self.get_queryset().filter(billing_status=True)

    def user_orders(self, user_id):
        """
        """
        return self.paid_orders().filter(user__id=user_id)

    def get_user_orders_products_ids(self, user_id):
        """
        """
        products_list_ids = []
        for order in self.user_orders(user_id):
            for item in order.items.all():
                if item.variation.product.id not in products_list_ids:
                    products_list_ids.append(item.variation.product.id)  
        return products_list_ids


class Order(BaseTimestamp):
    """
    Order model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', null=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    billing_status = models.BooleanField(default=False)
    shipping_status = models.BooleanField(default=False)

    objects = OrderManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return user's name and date of order creation. 
        return  f"{self.user.first_name} {self.user.last_name} | {self.created_at}"  


class OrderItem(BaseTimestamp):
    """
    Order item model.
    """
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='items', null=True)
    variation = models.ForeignKey("product.Variation", on_delete=models.SET_NULL, related_name='order_items', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # Return order item's id. 
        return  f"{self.id}"

    def get_total_price(self):
        # Return total price of all quantities.
        return self.price * self.quantity    


class ShippingAddress(BaseTimestamp):
    """
    Shipping address model.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address', null=True, blank=True)
    full_name = models.CharField(max_length=64)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return user's name and date of creation. 
        return  f"{self.full_name} | {self.created_at}"  