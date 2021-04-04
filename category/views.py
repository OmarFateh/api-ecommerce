from .models import Category
from .serializers import CategorySerializer, CategoryListSerializer

from rest_framework import generics, mixins, permissions


class CategoryListAPIView(generics.ListAPIView):
    """
    Category list API view.
    """
    queryset = Category.objects.root_nodes()
    serializer_class = CategoryListSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Category detail API view.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}