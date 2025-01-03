from django.urls import path
from .views import checkout, checkout_created, order_detail

app_name = 'orders'

urlpatterns = [
    path('create/', checkout, name='order_create'),
    path('created/', checkout_created, name='created'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]