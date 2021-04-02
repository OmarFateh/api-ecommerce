from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site

from product.base_serializers import ProductSerializer
from order.serializers import OrderSerializer
from .models import User
from .permissions import AnonPermissionOnly
from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer,
    PassowordChangeSerializer,
    PasswordResetEmailSerializer,
    PasswordResetSerializer,
    UserDetailSerializer, 
    UserReviewsSerializer,
)

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterAPIView(generics.CreateAPIView):
    """
    User registeration API view.
    """
    permission_classes = [AnonPermissionOnly]  
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}


class UserLoginAPIView(APIView):
    """
    User login API view.
    """
    permission_classes = [AnonPermissionOnly]  
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Override the post method and login user.
        """
        serializer = UserLoginSerializer(data=request.data, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """
    User logout API view.
    """
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        """
        Override the post method and logout user.
        """
        try:
            # add refresh token to blacklist
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("{'success':'You are logged out successfully.}", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PassowordChangeAPIView(generics.UpdateAPIView):
    """
    User profile update API view.
    """
    serializer_class = PassowordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Override the update method and update user's password.
        """
        serializer = PassowordChangeSerializer(request.user, data=request.data, partial=True, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"success":"Your password was changed successfully."}, status=status.HTTP_200_OK)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetEmailAPIView(APIView):
    """
    """
    def post(self, request, *args, **kwargs):
        """
        Override the post method and request password reset email.
        """
        serializer = PasswordResetEmailSerializer(data=request.data, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            # send email to user with reset password link.
            user = User.objects.get(email=request.data["email"])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = str(PasswordResetTokenGenerator().make_token(user))
            current_site = get_current_site(request).domain
            relative_link = reverse("users-api:password-reset-confirm", kwargs={"uidb64":uidb64, "token":token})
            absurl = f"http://{current_site}{relative_link}"
            email = EmailMessage(
                    f'Reset your Password', # subject  
                    f"""Hello {user.first_name} {user.last_name}, 
                    \nyou can use the link below to reset your password,
                    \n{absurl}""", # message
                    'fatehomar0@gmail.com', # from email
                    [user.email,] # to email list
                )
            email.send()
            return Response({"success":"We have sent you an email to reset your password."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetTokenCheckAPIView(APIView):
    """
    """
    def get(self, request, uidb64, token, *args, **kwargs):
        """
        """
        try:
            # decode the user's id and get the user by id.
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            # check if the token is valid.
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error":"Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"success":"Credintials are Valid", "uidb64":uidb64, "token":token}, status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({"error":"Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetFormAPIView(generics.GenericAPIView):
    """
    Password reset form API view.
    """
    serializer_class = PasswordResetSerializer

    def patch(self, request, *args, **kwargs):
        """
        Override the patch method and reset user's password.
        """
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"success":"Your password was changed successfully."}, status=status.HTTP_200_OK)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.UpdateAPIView):
    """
    User profile update API view.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Override the get method and data of current user.
        """
        serializer = UserDetailSerializer(request.user, context={"request": self.request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Override the update method and update user's data.
        """
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class UserDetailAPIView(generics.RetrieveAPIView):
    """
    User detail API view.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'


class MyReviewsListAPIView(APIView):
    """
    Reviews list of current user API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Override the get method and get reviews list of current user.
        """
        # get user reviews queryset.
        user_reviews = request.user.reviews.all()
        serializer = UserReviewsSerializer(user_reviews, many=True, context={"request": self.request})
        return Response(serializer.data)


class UserReviewsListAPIView(generics.ListAPIView):
    """
    User reviews list API view.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserReviewsSerializer

    def get_object(self, *args, **kwargs):
        # get user id from the requested url.
        user_id = self.kwargs.get("id", None)
        # get the user object by id.
        obj = get_object_or_404(User, id=user_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user reviews queryset.
        user_reviews = self.get_object().reviews.all()
        return user_reviews


class MyWishlistAPIView(APIView):
    """
    Wishlist of current user API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Override the get method and get wishlist of current user.
        """
        # get user wishlist queryset.
        user_wishlist = request.user.wishlist.all()
        serializer = ProductSerializer(user_wishlist, many=True, context={"request": self.request})
        return Response(serializer.data)


class UserWishlistAPIView(generics.ListAPIView):
    """
    User wishlist API view.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_object(self, *args, **kwargs):
        # get user id from the requested url.
        user_id = self.kwargs.get("id", None)
        # get the user object by id.
        obj = get_object_or_404(User, id=user_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user wishlist queryset.
        user_wishlist = self.get_object().wishlist.all()
        return user_wishlist


class MyOrderListAPIView(APIView):
    """
    Order list of current user API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Override the get method and get orders list of current user.
        """
        # get user orders queryset.
        user_orders = request.user.orders.all()
        serializer = OrderSerializer(user_orders, many=True, context={"request": self.request})
        return Response(serializer.data)

