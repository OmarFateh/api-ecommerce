from product.mixins import TimestampMixin
from product.serializers import VariationDetailSerializer
from accounts.base_serializers import UserSerializer
from .models import Order, OrderItem, ShippingAddress

from rest_framework import serializers


class ShippingAddressSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Shipping address model serializer.
    """
    class Meta:
        model  = ShippingAddress
        fields = ["id", "full_name", "address1", "address2", "city", "phone", "postal_code"]


class OrderItemSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Order item model serializer.
    """
    variation = VariationDetailSerializer(read_only=True)

    class Meta:
        model  = OrderItem
        fields = ["id", "variation", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Order model serializer.
    """
    user = UserSerializer()
    orders = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    
    class Meta:
        model  = Order
        fields = ["id", "user", "orders", "shipping_address", "total_paid", "billing_status", "shipping_status"]

    def get_orders(self, obj):
        """
        Get order's items.
        """
        items = obj.items.all()
        if items:
            return OrderItemSerializer(items, many=True).data
        else:
            return None

    def get_shipping_address(self, obj):
        """
        Get shipping address.
        """ 
        if obj.shipping_address:
            return ShippingAddressSerializer(obj.shipping_address, many=False).data
        else:
            return None       