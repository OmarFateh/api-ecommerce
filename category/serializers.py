from product.mixins import TimestampMixin
from product.models import Product
from product.base_serializers import ProductSerializer
from .models import Category

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Category model serializer.
    """
    children_categories = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "products", "children_categories", "updated_at", "created_at"]

    def get_products(self, obj):
        context = self.context
        request = context.get('request')
        # get all products of descendants categories of this category
        products = Product.objects.get_descendants_products(obj)
        if products:
            return ProductSerializer(products, many=True, context={'request': request}).data
        else:
            return None    
        
    def get_children_categories(self, obj):
        if obj.get_children():
            return CategorySerializer(obj.get_children(), many=True, context=self.context).data
        else:
            return None

# CategorySerializer._declared_fields['children'] = CategorySerializer(many=True)


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category list model serializer.
    """
    children_categories = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "children_categories"]

    def get_children_categories(self, obj):
        if obj.get_children():
            return CategoryListSerializer(obj.get_children(), many=True, context=self.context).data
        else:
            return None    

# CategoryListSerializer._declared_fields['children'] = CategoryListSerializer(many=True)        