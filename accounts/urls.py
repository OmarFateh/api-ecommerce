from django.urls import path

from .views import (
    UserRegisterAPIView, 
    UserLoginAPIView,
    UserLogoutAPIView,
    PassowordChangeAPIView,
    PasswordResetEmailAPIView,
    PasswordResetTokenCheckAPIView, 
    PasswordResetFormAPIView,
    UserProfileAPIView,
    UserDetailAPIView, 
    MyReviewsListAPIView,
    UserReviewsListAPIView,
    MyWishlistAPIView, 
    UserWishlistAPIView,
    MyOrderListAPIView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


"""
CLIENT
BASE ENDPOINT /api/users/
"""

urlpatterns = [
    # Authentications
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    # Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Password
    path('password/change/', PassowordChangeAPIView.as_view(), name='password-change'),
    path('password/reset/', PasswordResetEmailAPIView.as_view(), name='password-reset'),
    path('password/reset/<uidb64>/<token>/', PasswordResetTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password/reset/complete/', PasswordResetFormAPIView.as_view(), name='password-reset-complete'),
    # Profile
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('<int:id>/', UserDetailAPIView.as_view(), name='detail'),
    # Reviews
    path('profile/reviews/list/', MyReviewsListAPIView.as_view(), name='profile-reviews-list'),
    path('<int:id>/reviews/list/', UserReviewsListAPIView.as_view(), name='reviews-list'),
    # Wishlist
    path('profile/wishlist/', MyReviewsListAPIView.as_view(), name='profile-wishlist'),
    path('<int:id>/wishlist/', UserWishlistAPIView.as_view(), name='wishlist'),
    # orders
    path('profile/orders/', MyOrderListAPIView.as_view(), name='profile-orders'),

]