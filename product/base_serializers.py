from .models import Product, Variation

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """
    Product model serializer.
    """
    url = serializers.HyperlinkedIdentityField(view_name='product-api:detail', lookup_field='id')

    class Meta:
        model  = Product
        fields = ["id", "name", "regular_price", "sale_price", "url"]


class VariationSerializer(serializers.ModelSerializer):
    """
    Variation model serializer.
    """
    class Meta:
        model  = Variation
        fields = ["id", "color", "size", "images", "regular_price", "sale_price", "quantity"]