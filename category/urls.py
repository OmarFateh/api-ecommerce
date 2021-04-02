from django.urls import path

from .views import CategoryListAPIView, CategoryDetailAPIView

"""
CLIENT
BASE ENDPOINT /api/categories/
"""

urlpatterns = [
    path('list/', CategoryListAPIView.as_view(), name='list'),
    path('<int:id>/', CategoryDetailAPIView.as_view(), name='detail'),

]