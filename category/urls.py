from django.urls import path

from .views import CategoryListAPIView, RootCategoryListAPIView, CategoryDetailAPIView

"""
CLIENT
BASE ENDPOINT /api/categories/
"""

urlpatterns = [
    path('list/', CategoryListAPIView.as_view(), name='list'),
    path('root/list/<int:id>/', RootCategoryListAPIView.as_view(), name='root-list'),
    path('<int:id>/', CategoryDetailAPIView.as_view(), name='detail'),

]