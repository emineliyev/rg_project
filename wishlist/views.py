# 1. Django и сторонние библиотеки
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

# 2. Импорты из проекта
from cart.cart import Cart
from shop.models import Product
from .wishlist import Wishlist


@require_POST
def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.add(product)
    return redirect('wishlist:wishlist_detail')


@require_POST
def wishlist_remove(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.remove(product)
    return redirect('wishlist:wishlist_detail')


def wishlist_detail(request):
    wishlist = Wishlist(request)
    cart = Cart(request)  # Если используется в этом же представлении
    return render(request, 'wishlist/wishlist_detail.html', {
        'wishlist': wishlist,
        'cart': cart
    })
