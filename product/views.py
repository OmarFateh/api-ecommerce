from django.shortcuts import get_object_or_404

from .models import Product, ProductReview
from .base_serializers import ProductSerializer
from .serializers import ProductDetailSerializer, ProductReviewsListSerializer, UserReviewSerializer, UserReviewUpdateSerializer
from .permissions import UserCreateReviewPermission, UserUpdateDeleteReviewPermission
from accounts.permissions import AnonPermissionOnly

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductListAPIView(generics.ListAPIView):
    """
    Product list API view.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Product detail list API view.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

        
class ProductReviewsListAPIView(generics.ListAPIView):
    """
    Product reviews list API view.
    """
    serializer_class = ProductReviewsListSerializer

    def get_object(self, *args, **kwargs):
        # get product id from the requested url.
        product_id = self.kwargs.get("id", None)
        # get the product object by id.
        obj = get_object_or_404(Product, id=product_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get product reviews queryset.
        product_reviews = self.get_object().reviews.all()
        return product_reviews


class CreateProductReviewAPIView(APIView):
    """
    Create Product review of current user API view.
    """
    serializer_class = UserReviewSerializer
    permission_classes = [UserCreateReviewPermission]

    def get_object(self, *args, **kwargs):
        # get product id from the requested url.
        product_id = self.kwargs.get("id", None)
        # get the product review object of current user.
        try:
            obj = ProductReview.objects.get(user=self.request.user, product_id=product_id)
        except:
            obj = None    
        # check object permissions.
        self.check_object_permissions(self.request, product_id)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Override the get method and get product's review of current user.
        """
        # get user's review for a product.
        serializer = UserReviewSerializer(self.get_object(), context={"request": self.request})
        return Response(serializer.data)
 
    def post(self, request, *args, **kwargs):
        """
        Override the post method and create product's review of current user.
        """
        data = request.data
        user_review = ProductReview.objects.create(
            user = request.user, 
            product_id = self.kwargs['id'], 
            rate = data.get('rate'),
            title = data.get("title"), 
            content = data.get("content"), 
        )
        serializer = UserReviewSerializer(user_review, context={"request": self.request})
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class UpdateDeleteProductReviewAPIView(generics.UpdateAPIView, APIView):
    """
    Update delete product's review of current user API view.
    """
    serializer_class = UserReviewSerializer
    permission_classes = [UserUpdateDeleteReviewPermission]
    
    def get_object(self, *args, **kwargs):
        # get product id from the requested url.
        product_id = self.kwargs.get("id", None)
        # get the product review object of current user.
        try:
            obj = ProductReview.objects.get(user=self.request.user, product_id=product_id)
        except:
            obj = None
        # check object permissions.
        self.check_object_permissions(self.request, product_id)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Override the get method and get product's review of current user.
        """
        # get user's review for a product.
        serializer = UserReviewSerializer(self.get_object(), context={"request": self.request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Override the update method and update product's review of current user.
        """
        serializer = UserReviewUpdateSerializer(self.get_object(), data=request.data, partial=True, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, *args, **kwargs):
        """
        Override the delete method and delete product's review of current user.
        """ 
        self.get_object().delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddDeleteProductWishlistAPIView(APIView):
    """
    Add delete product wishlist API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        # get product id from the requested url.
        product_id = self.kwargs.get("id", None)
        # get the product object by id.
        obj = get_object_or_404(Product, id=product_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Add or delete product to or from the user's wishlist.
        """ 
        data = request.data
        product = self.get_object()
        if product.favourites.filter(id=request.user.id).exists():
            product.favourites.remove(request.user)
            return Response({'success':'this product was deleted successfully from your wishlist.'}, status=status.HTTP_200_OK)
        else:    
            product.favourites.add(request.user)
            return Response({'success':'this product was added successfully to your wishlist.'}, status=status.HTTP_200_OK)