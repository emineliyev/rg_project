# 1. Встроенные библиотеки Python
from decimal import Decimal

# 2. Сторонние библиотеки Django
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

# 3. Импорты из проекта
from shop.models import WeightOption
from .models import Order, OrderItem
from .forms import OrderForm, SalesFilterForm
from cart.cart import Cart
from .tasks import notify_low_stock, notify_new_order, generate_and_send_order_pdf



@login_required
def checkout(request):
    """
    Представление заказа
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            order = form.save(commit=False)

            # Привязываем пользователя и email
            if request.user.is_authenticated:
                order.user = request.user
                order.email = request.user.email

            # Применяем купон, если он есть
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount  # Сохраняем процент скидки

                cart.coupon.used_by_fin_codes.add(request.user)
                cart.coupon.save()

            # Расчёт итоговой суммы
            total_price_before_discount = cart.get_total_price()  # Сумма до скидки
            discount_amount = cart.get_discount()  # Сумма скидки
            total_price_after_discount = total_price_before_discount - discount_amount

            # Устанавливаем итоговую сумму
            order.total_price = total_price_after_discount

            order.save()

            for item in cart:
                product = item['product']
                quantity = item['quantity']
                weight_option = item.get('weight_option')

                weight_option_obj = None
                if weight_option:
                    weight_option_obj = WeightOption.objects.get(id=weight_option['id'])

                # Рассчитываем цену товара с учётом скидки купона
                discounted_price = product.discounted_price
                weight_modifier = Decimal(weight_option['price_modifier']) if weight_option else 0
                total_item_price = discounted_price + weight_modifier

                # Применяем скидку купона, если он есть
                if cart.coupon:
                    total_item_price -= total_item_price * (cart.coupon.discount / Decimal(100))

                # Сохраняем элемент заказа
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=total_item_price,
                    quantity=quantity,
                    weight_option=weight_option_obj
                )

                # Обновляем количество товара на складе
                product.quantity_in_stock -= quantity

                product.popularity += 1

                product.save()

                # Уведомляем об остатке
                if product.quantity_in_stock <= 3:
                    notify_low_stock.delay(product.name, product.article, product.quantity_in_stock)

            # Уведомления и очистка корзины
            notify_new_order.delay(order.id)
            generate_and_send_order_pdf.delay(order.id)
            cart.clear()

            # Удаление купона из сессии
            if 'coupon_id' in request.session:
                del request.session['coupon_id']  # Удаляем купон из сессии

            return redirect('orders:created')

    else:
        form = OrderForm(user=request.user if request.user.is_authenticated else None)

    # Вычисляем общую сумму и скидку для отображения в форме
    total_price = cart.get_total_price()
    total_discount = cart.get_discount()
    total_price_after_discount = cart.get_total_price_after_discount()

    return render(request, 'orders/create.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
        'total_discount': total_discount,
        'total_price_after_discount': total_price_after_discount,
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
    """
    Представление об успешном заказе
    """
    return render(request, 'orders/created.html')


@staff_member_required
def sales_chart(request):
    """
    Отображаем график покупок в админке
    """
    form = SalesFilterForm(request.GET or None)
    orders = Order.objects.all()

    # Применяем фильтры
    if form.is_valid():
        year = form.cleaned_data.get('year')
        month = form.cleaned_data.get('month')
        day = form.cleaned_data.get('day')

        if year:
            orders = orders.filter(created_at__year=year)
        if month:
            orders = orders.filter(created_at__month=month)
        if day:
            orders = orders.filter(created_at__day=day)

    # Группируем данные по месяцам
    sales_data = (
        orders.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('month')
    )

    # Подготавливаем данные для графика
    labels = [data['month'].strftime('%Y-%m') for data in sales_data]
    sales = [float(data['total_sales']) for data in sales_data]

    return render(request, 'admin/sales_chart.html', {
        'form': form,
        'labels': labels,
        'sales': sales,
    })
