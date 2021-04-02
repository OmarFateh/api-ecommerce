from django.urls import path

from .views import CreateOrderAPIView

"""
CLIENT
BASE ENDPOINT /api/orders/
"""

urlpatterns = [
    path('add/', CreateOrderAPIView.as_view(), name='add'),
]