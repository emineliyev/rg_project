from django.urls import path
from .views import (
    HomeProductListView, ProductDetailView, ProductListView, ContactListView, CategoryProductListView
)

app_name = 'shop'

urlpatterns = [
    path('', HomeProductListView.as_view(), name='index'),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='products'),
    path('contact/', ContactListView.as_view(), name='contact'),

    path('category/<slug:slug>/', CategoryProductListView.as_view(), name='category'),

]
