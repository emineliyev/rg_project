from decimal import Decimal

from django.shortcuts import get_object_or_404

from shop.models import WeightOption
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart

from .tasks import notify_low_stock, notify_new_order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def checkout(request):
    cart = Cart(request)  # Получаем корзину
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Создаем записи OrderItem для каждого товара в корзине
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                weight_option = item.get('weight_option')  # Это словарь или None

                # Получаем объект WeightOption, если вес был выбран
                weight_option_obj = None
                if weight_option:
                    weight_option_obj = WeightOption.objects.get(id=weight_option['id'])

                # Рассчитываем итоговую цену с учетом модификатора веса
                discounted_price = product.discounted_price
                weight_modifier = Decimal(weight_option['price_modifier']) if weight_option else 0
                total_item_price = discounted_price + weight_modifier

                # Создаём OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=total_item_price,
                    quantity=quantity,
                    weight_option=weight_option_obj  # Сохраняем выбранный вес
                )

                # Уменьшаем количество на складе
                product.quantity_in_stock -= quantity
                product.save()

                # Если остаток на складе меньше 3, запускаем задачу уведомления
                if product.quantity_in_stock <= 3:
                    notify_low_stock.delay(product.name, product.article, product.quantity_in_stock)

            # Запускаем задачу уведомления о новом заказе
            notify_new_order.delay(order.id)

            # Очищаем корзину
            cart.clear()

            return redirect('orders:created')
    else:
        form = OrderForm(user=request.user if request.user.is_authenticated else None)

    # Рассчитываем общую сумму корзины и скидку
    total_price = sum(
        (item['product'].discounted_price +
         Decimal(item['weight_option']['price_modifier']) if item.get('weight_option') else 0) * item['quantity']
        for item in cart
    )
    total_discount = sum(
        ((item['product'].price - item['product'].discounted_price) * item['quantity'])
        for item in cart
    )

    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
        'total_discount': total_discount
    })


@login_required
def order_detail(request, order_id):
    """
    Отображает детальную страницу заказа.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    order_items = order.items.select_related('product')
    total_price = sum(item.quantity * item.price for item in order_items)

    return render(request, 'orders/detail.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
    })


def checkout_created(request):
    return render(request, 'orders/created.html')
