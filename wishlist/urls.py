from django.urls import path
from .views import wishlist_detail, wishlist_add, wishlist_remove

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_detail, name='wishlist_detail'),
    path('add_wish/<int:product_id>/', wishlist_add, name='add_wish'),
    path('remove/<int:product_id>/', wishlist_remove, name='wishlist_remove'),
]
