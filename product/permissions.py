from order.models import Order
from product.models import ProductReview

from rest_framework.permissions import BasePermission


class UserCreateReviewPermission(BasePermission):
    """
    A custom permission for adding a product's review.
    Allow only the users who have ordered this product to add only one review.
    """
    message = "You need to order this product first to add a review."

    def has_permission(self, request, view, *args, **kwargs):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj in Order.objects.get_user_orders_products_ids(request.user.id):
            if ProductReview.objects.filter(user=request.user, product_id=obj).exists():
                # can't post a new one
                self.message = "You already have a review for this product."
                return False    
            else:
                return True
        else:
            return False    


class UserUpdateDeleteReviewPermission(BasePermission):
    """
    A custom permission for adding a product's review.
    Allow only the users who have ordered this product and have a review to update or delete it.
    """
    message = "You need to order this product first to add a review."

    def has_permission(self, request, view, *args, **kwargs):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj in Order.objects.get_user_orders_products_ids(request.user.id):
            if ProductReview.objects.filter(user=request.user, product_id=obj).exists():
                return True    
            else:
                # can't update or delete
                self.message = "You need to add a review for this product first."
                return False
        else:
            return False    