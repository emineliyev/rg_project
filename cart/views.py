from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupons.models import Coupon
from shop.models import Product, WeightOption


@require_POST
def cart_add(request, product_id):
    """
    Добавляем товар в корзину
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    weight_option_id = request.POST.get('weight_option')
    weight_option = None

    if weight_option_id:
        weight_option = get_object_or_404(WeightOption, id=weight_option_id)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, weight_option=weight_option, quantity=cd['quantity'], override_quantity=True)

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Удаляем товар из-корзину
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Отображаем детальную страницу корзины
    """
    cart = Cart(request)
    applied_coupon = None
    if 'coupon_id' in request.session:
        applied_coupon = Coupon.objects.filter(id=request.session['coupon_id']).first()
    total_discount = sum(
        ((item['product'].price - item['product'].discounted_price) * item['quantity'])
        for item in cart
    )
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override_quantity': True
        })
    coupon_apply_form = CouponApplyForm()
    context = {
        'cart': cart,
        'total_discount': total_discount,
        'coupon_apply_form': coupon_apply_form,
        'applied_coupon': applied_coupon
    }
    return render(request, 'cart/detail.html', context=context)


def cart_clear(request):
    """
    Очищаем корзину
    """
    cart = request.session.get('cart')
    if cart:
        # Səbəti sessiyadan çıxardır
        # Удаляем корзину из сессии
        # Remove the basket from the session
        del request.session['cart']
        # Ayrılıqda saxlanan, cəmi sıfırlayır
        # Сбрасывает общую сумму, если она сохранена отдельно
        # Resets the total amount if it is stored separately
        request.session['cart_total'] = 0
    # Səbət səhifəsinə və ya başqa səhifəyə yönləndirir
    # Перенаправляет на страницу корзины или другую страницу
    # Redirects to the cart page or another page
    return redirect('cart:cart_detail')
