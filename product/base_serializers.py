from .models import Product, Variation, ProductReview, ProductImage

from rest_framework import serializers
 

class ProductBaseSerializer(serializers.ModelSerializer):
    """
    Product base model serializer.
    """
    rate = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = ["rate", "reviews_count", "is_in_wishlist"]
        
    def get_rate(self, obj):
        """
        Get product's rate.
        """
        return ProductReview.objects.get_avg_rate(obj.id)
        
    def get_reviews_count(self, obj):
        """
        Get product's reviews count.
        """
        return obj.reviews.count()

    def get_is_in_wishlist(self, obj):
        """
        Check if the product is in current user's wishlist.
        """
        context = self.context
        request = context['request']
        if request.user.is_authenticated:
            return obj.favourites.filter(id=request.user.id).exists()
        else:
            return False    


class ProductSerializer(ProductBaseSerializer):
    """
    Product list model serializer.
    """
    thumbnail = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='product-api:detail', lookup_field='id')

    class Meta:
        model  = Product
        fields = ["id", "name", "regular_price", "sale_price", "description", "rate", "reviews_count", 
            "is_in_wishlist", "thumbnail", "url"
        ]

    # def get_thumbnail(self, obj):
    #     """
    #     Get product's thumbnail.
    #     """
    #     return obj.thumbnail.url

    def get_thumbnail(self, obj):
        """
        Get product's thumbnail.
        """
        return ProductImage.objects.get_product_thumbnail(obj.id)


class VariationSerializer(serializers.ModelSerializer):
    """
    Variation model serializer.
    """
    class Meta:
        model  = Variation
        fields = ["id", "color", "size", "images", "regular_price", "sale_price", "quantity"]