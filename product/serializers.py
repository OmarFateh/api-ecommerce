from accounts.base_serializers import UserSerializer
from .models import Product, Variation, ProductColor, ProductSize, ProductImage, ProductReview
from .mixins import TimestampMixin
from .base_serializers import ProductBaseSerializer

from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Product Image model serializer.
    """
    class Meta:
        model  = ProductImage
        fields = ["id", "image", "thumbnail", "active"]


class ProductSizeSerializer(serializers.ModelSerializer):
    """
    Product Size model serializer.
    """
    class Meta:
        model  = ProductSize
        fields = ["id", "name"]


class ProductColorSerializer(serializers.ModelSerializer):
    """
    Product Color model serializer.
    """
    class Meta:
        model  = ProductColor
        fields = ["id", "name", "code"]


class VariationDetailSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Product Variation detail model serializer.
    """
    color = ProductColorSerializer()
    size = ProductSizeSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model  = Variation
        fields = ["id", "color", "size", "images", "regular_price", "sale_price", 
            "quantity", "in_stock", "active", "updated_at", "created_at"
        ]


class ProductDetailSerializer(ProductBaseSerializer, TimestampMixin):
    """
    Product detail model serializer.
    """
    variations = VariationDetailSerializer(many=True, read_only=True)
    reviews_url = serializers.HyperlinkedIdentityField(view_name='product-api:reviews-list', lookup_field='id')

    class Meta:
        model  = Product
        fields = ["id", "name", "slug", "description", "details", "regular_price", "sale_price", "rate", 
            "reviews_count", "quantity", "variations", "reviews_url", "in_stock", "active", "is_in_wishlist",
            "updated_at", "created_at"
        ]

    
class ProductReviewsListSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Product reviews list model serializer.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model  = ProductReview
        fields = ["id", "user", "title", "content", "rate", "updated_at", "created_at"]


class UserReviewSerializer(serializers.ModelSerializer, TimestampMixin):
    """
    User review model serializer.
    """
    class Meta:
        model  = ProductReview
        fields = ["id", "title", "content", "rate", "updated_at", "created_at"]

   
class UserReviewUpdateSerializer(serializers.ModelSerializer):
    """
    User review model serializer.
    """
    class Meta:
        model  = ProductReview
        fields = ["id", "title", "content", "rate"]

    def update(self, instance, validated_data):
        """
        Update user's review.
        """
        if validated_data.get('title'):
            instance.title = validated_data.get('title')
        if validated_data.get('content'):
            instance.content = validated_data.get('content')
        if validated_data.get('rate'):
            instance.rate = validated_data.get('rate')
        instance.save()
        return validated_data