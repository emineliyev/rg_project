# 1. Встроенные библиотеки Python
import os
from decimal import Decimal

# 2. Сторонние библиотеки
import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

# 3. Импорты из проекта
from orders.models import Order, OrderItem


@shared_task
def notify_low_stock(product_name, product_article, quantity_in_stock):
    """
    Уведомляет администраторов о низком уровне товара.
    """
    subject = f"Stok xəbərdarlığı: {product_name}"
    message = f"'{product_name}' məhsulunun (Article: {product_article}) ehtiyatı tükənir cəmi {quantity_in_stock} ədəd qaldı"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin[1] for admin in settings.ADMINS],
    )


@shared_task
def notify_new_order(order_id):
    """
    Уведомляет администраторов о новом заказе.
    """
    from .models import Order  # Импорт внутри функции для избегания циклических зависимостей

    try:
        # Получаем заказ по ID
        order = Order.objects.get(id=order_id)
        # Получаем все элементы заказа
        items = order.items.select_related('product')  # Используем select_related для оптимизации запросов

        if not items.exists():
            return  # Если у заказа нет элементов, уведомление не отправляем

        # Формируем список товаров
        items_details = "\n".join(
            [
                f"{item.product.name} x {item.quantity} hər biri ({item.price} ₼)"
                for item in items
            ]
        )

        # Проверяем общую сумму заказа
        total_price = sum(item.quantity * item.price for item in items)

        # Формируем детали заказа
        order_details = f"""
        Yeni sifariş alındı:

        Sifariş ID: {order.id}
        Müştəri: {order.first_name} {order.last_name}
        E-poçt: {order.email}
        Telefon: {order.phone_number}
        Ünvan: {order.address}, {order.city}, {order.country}

        Əşyalar:
        {items_details}

        Cəmi: {total_price}₼
        """

        # Отправляем email администраторам
        send_mail(
            subject=f"Yeni Sifariş #{order.id}",
            message=order_details,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin[1] for admin in settings.ADMINS],
        )
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} does not exist.")


@shared_task
def generate_and_send_order_pdf(order_id):
    """
    PDF заказа для покупателя
    """
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    # Подготавливаем данные для PDF
    items_with_discount = []
    for item in order_items:
        original_price = item.product.price  # Оригинальная цена продукта
        weight_modifier = item.weight_option.price_modifier if item.weight_option else Decimal(0)  # Учёт веса
        original_price_with_weight = original_price + weight_modifier  # Цена с учётом веса

        discounted_price = item.price  # Итоговая цена, сохранённая в OrderItem
        discount = original_price_with_weight - discounted_price  # Сумма скидки

        items_with_discount.append({
            'product': item.product,
            'quantity': item.quantity,
            'original_price': original_price_with_weight,
            'discounted_price': discounted_price,
            'discount': discount,
        })

    # Подготавливаем HTML-шаблон
    html = render_to_string('orders/pdf.html', {
        'order': order,
        'order_items': items_with_discount,
        'total_price': order.total_price,  # Итоговая сумма со скидкой
    })

    # Генерация PDF
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "orders")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    pdf_file_path = os.path.join(pdf_dir, f'order_{order_id}.pdf')

    weasyprint.HTML(string=html).write_pdf(pdf_file_path)

    # Отправляем PDF по почте
    user_email = order.user.email if order.user else order.email
    subject = f"Sifariş təsdiqi #{order.id}"
    message = f"""
    Hörmətli {order.first_name} {order.last_name},

    Sifarişiniz təsdiqləndi! PDF faktura əlavə olunmuşdur.

    Sifariş №: RG-{order.id}
    Məbləğ: {order.total_price} ₼

    Hörmətlə, Rafig Jewellery!
    """
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    email.attach_file(pdf_file_path)
    email.send()
