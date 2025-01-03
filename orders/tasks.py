from celery import shared_task
from django.core.mail import send_mail
from core import settings


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
