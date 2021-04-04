from django.urls import path

from .views import (
    # ProductListAPIView, 
    ProductDetailAPIView, 
    ProductReviewsListAPIView, 
    CreateProductReviewAPIView,
    UpdateDeleteProductReviewAPIView,
    AddDeleteProductWishlistAPIView,
)

"""
CLIENT
BASE ENDPOINT /api/products/
"""

urlpatterns = [
    # Products
    # path('list/', ProductListAPIView.as_view(), name='list'),
    path('<int:id>/', ProductDetailAPIView.as_view(), name='detail'),
    # Reviews
    path('<int:id>/reviews/list/', ProductReviewsListAPIView.as_view(), name='reviews-list'),
    path('<int:id>/review/add/', CreateProductReviewAPIView.as_view(), name='add-review'),
    path('<int:id>/review/update/delete/', UpdateDeleteProductReviewAPIView.as_view(), name='update-delete-review'),
    # wishlist
    path('<int:id>/wishlist/add/delete/', AddDeleteProductWishlistAPIView.as_view(), name='add-delete-wishlist'),
]