from django.urls import path
from .views import index, product_detail, product_list

app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('product-detail/', product_detail, name='product_detail'),
    path('products/', product_list, name='product_list'),
]