from django.urls import path
from .views import (
    ProductListView, ProductDetailView
)

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
