from product.mixins import TimestampMixin
from product.models import Product
from product.base_serializers import ProductSerializer
from .models import Category

from rest_framework import serializers



class RootCategorySerializer(serializers.ModelSerializer):
    """
    Root Category list model serializer.
    """
    children_categories = serializers.SerializerMethodField()
    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "children_categories"]
    
    def get_children_categories(self, obj):
        if obj.get_children():
            return RootCategorySerializer(obj.get_children(), many=True, context=self.context).data
        else:
            return None

class ChildrenCategorySerializer(serializers.ModelSerializer):
    """
    Children Category list model serializer.
    """
    class Meta:
        model  = Category
        fields = ["id", "name", "slug"]


class CategorySerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Category model serializer.
    """
    root_category = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    # category_list = serializers.SerializerMethodField()
    # parent_categories = serializers.SerializerMethodField()
    # siblings_categories = serializers.SerializerMethodField()
    # children_categories = serializers.SerializerMethodField()
    # "parent_categories", "siblings_categories", "children_categories", 
    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "root_category", "products", "updated_at", "created_at"]

    def get_root_category(self, obj):
        if not obj.is_root_node():
            return ChildrenCategorySerializer(obj.get_root(), context=self.context).data
        else:
            return None

    def get_products(self, obj):
        context = self.context
        request = context.get('request')
        # get all products of descendants categories of this category
        products = Product.objects.get_descendants_products(obj)
        if products:
            return ProductSerializer(products, many=True, context={'request': request}).data
        else:
            return None    
    # - Men --> root_node
    #     -- Clothing --> not root_node & obj.get_children
    #         --- jackets --> not root_node & not obj.get_children
    #         --- Coats
    #     -- Shoes
    # def get_category_list(self, obj):
    #     if obj.is_root_node():
    #         print('yess')
    #         return CategorySerializer(obj.get_children(), many=True, context=self.context).data
    #     if obj.get_children():
    #         return CategorySerializer(obj.get_children(), many=True, context=self.context).data
    #     else:
    #         return ChildrenCategorySerializer(obj.get_root().get_children(), many=True, context=self.context).data     

    # def get_parent_categories(self, obj):
    #     if obj.is_root_node():
    #         return None
    #     elif not obj.is_root_node() and not obj.get_children():
    #         print('yess')
    #         return CategorySerializer(obj.get_parent(), context=self.context).data
    #     elif not obj.is_root_node() and obj.get_children():
    #         return ChildrenCategorySerializer(obj.get_parent(), context=self.context).data
    #     else:
    #         return None

    # def get_siblings_categories(self, obj):
    #     if not obj.is_root_node() and obj.get_siblings():
    #         return ChildrenCategorySerializer(obj.get_siblings(), many=True, context=self.context).data
    #     else:
    #         return None

    # def get_children_categories(self, obj):
    #     if obj.get_children() and obj.is_root_node():
    #         return CategorySerializer(obj.get_children(), many=True, context=self.context).data
    #     elif obj.get_children():
    #         return ChildrenCategorySerializer(obj.get_children(), many=True, context=self.context).data
    #     else:
    #         return None

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
            return ChildrenCategorySerializer(obj.get_children(), many=True, context=self.context).data
        else:
            return None    

# CategoryListSerializer._declared_fields['children'] = CategoryListSerializer(many=True)        