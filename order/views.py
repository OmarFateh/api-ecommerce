from django.shortcuts import get_object_or_404

from product.models import Variation
from .serializers import OrderSerializer
from .models import Order, OrderItem, ShippingAddress

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


class CreateOrderAPIView(generics.CreateAPIView):
    """
    Create Order API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        """
        Override the post method and create new order.
        """
        data = request.data
        orderItems = data.get('orderItems')
        # check if there's order items
        if orderItems and len(orderItems) == 0:
            return Response({'message':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
        else:    
            # create order
            order = Order.objects.create(
                user = request.user,
                total_paid = data.get('total_paid'),
                billing_status = data.get('billing_status'),
                shipping_status = data.get('shipping_status'), 
            )
            # create shipping address
            shipping = ShippingAddress.objects.create(
                order = order,
                full_name = data.get('full_name'),
                address1 = data.get('address1'),
                address2 = data.get('address2'),
                city = data.get('city'),
                phone = data.get('phone'),
                postal_code = data.get('postal_code')
            )
            # create order items & set order to OrderItem relationship
            for item in orderItems:
                order_item = OrderItem.objects.create(
                        order = order,
                        variation = item['variation_id'],
                        price = item['price'],
                        quantity = item['qty'],
                    )
                # update variation qty in stock
                item_variation = get_object_or_404(Variation, id=item['variation_id'])
                item_variation.quantity -= order_item.quantity
                # update product qty in stock
                item_variation.product.quantity -= order_item.quantity
                item_variation.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

