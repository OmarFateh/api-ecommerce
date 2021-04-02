from product.mixins import TimestampMixin
from .models import Category

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer, TimestampMixin):
    """
    Category model serializer.
    """
    children_categories = serializers.SerializerMethodField()
    
    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "children_categories", "updated_at", "created_at"]

    def get_children_categories(self, obj):
        if obj.get_children():
            return CategorySerializer(obj.get_children(), many=True).data
        else:
            return None

# CategorySerializer._declared_fields['children'] = CategorySerializer(many=True)


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category list model serializer.
    """
    url = serializers.HyperlinkedIdentityField(view_name='category-api:detail', lookup_field='id')
    children_categories = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ["id", "name", "url", "children_categories"]

    def get_children_categories(self, obj):
        if obj.get_children():
            return CategoryListSerializer(obj.get_children(), many=True, context=self.context).data
        else:
            return None    

# CategoryListSerializer._declared_fields['children'] = CategoryListSerializer(many=True)        