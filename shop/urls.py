from django.urls import path
from .views import (
    HomeProductListView, ProductDetailView, ProductListView
)

app_name = 'shop'

urlpatterns = [
    path('', HomeProductListView.as_view(), name='index'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='products'),
]
