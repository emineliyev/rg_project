from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from .tasks import notify_low_stock, notify_new_order


@receiver(post_save, sender=OrderItem)
def reduce_stock_and_trigger_tasks(sender, instance, created, **kwargs):
    if created:  # Только при создании нового OrderItem
        product = instance.product
        product.quantity_in_stock -= instance.quantity
        product.save()

        # Запускаем задачу уведомления о низком уровне товара
        if product.quantity_in_stock <= 3:
            notify_low_stock.delay(product.name, product.article, product.quantity_in_stock)

        # Запускаем задачу уведомления о новом заказе
        order = instance.order
        notify_new_order.delay(order.id)
