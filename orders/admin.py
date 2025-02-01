# 1. Встроенные библиотеки Python
from decimal import Decimal

# 2. Django и сторонние библиотеки
from django.contrib import admin
from django.urls import reverse

# 3. Импорты из проекта
from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    verbose_name_plural = 'Məhsullar'
    readonly_fields = [
        'display_weight',
        'display_total_discount',
        'display_final_price',
        'display_original_price',
    ]

    def display_weight(self, obj):
        """
        Отображает выбранный вес, если он есть.
        """
        if getattr(obj, 'weight_option', None):
            return f"{obj.weight_option.weight} q"
        return "Çəki seçilməyib"

    display_weight.short_description = "Seçilən çəki"

    def display_total_discount(self, obj):
        """
        Отображает общую скидку (магазин + купон).
        """
        # Скидка магазина
        product_discount_percent = obj.product.discount
        product_discount = obj.product.price * Decimal(product_discount_percent) / Decimal(100)

        # Скидка купона
        coupon_discount_percent = Decimal(obj.order.discount or 0)
        weight_modifier = Decimal(obj.weight_option.price_modifier) if obj.weight_option else Decimal(0)
        discounted_price_with_weight = obj.product.discounted_price + weight_modifier
        coupon_discount = discounted_price_with_weight * coupon_discount_percent / Decimal(100)

        total_discount = (product_discount + coupon_discount) * obj.quantity

        return f"{total_discount:.2f} ₼ ({product_discount_percent}% mağaza, {coupon_discount_percent}% kupon)"

    display_total_discount.short_description = "Ümumi endirim"

    def display_final_price(self, obj):
        """
        Отображает итоговую цену со всеми скидками.
        """
        weight_modifier = Decimal(obj.weight_option.price_modifier) if obj.weight_option else Decimal(0)
        base_discounted_price = obj.product.discounted_price + weight_modifier

        if obj.order and obj.order.coupon:
            coupon_discount = Decimal(obj.order.discount) / Decimal(100)
            base_discounted_price -= base_discounted_price * coupon_discount

        total_price = base_discounted_price * obj.quantity
        return f"{total_price:.2f} ₼"

    display_final_price.short_description = "Son qiymət"

    def display_original_price(self, obj):
        """
        Отображает цену без скидки.
        """
        weight_modifier = Decimal(obj.weight_option.price_modifier) if obj.weight_option else Decimal(0)
        original_price_with_weight = (obj.product.price + weight_modifier) * obj.quantity
        return f"{original_price_with_weight:.2f} ₼"

    display_original_price.short_description = "Tam qiymət (çəki ilə)"

    # Переопределим метод для рендеринга дополнительной строки
    def get_extra(self, request, obj=None, **kwargs):
        return 0  # Убираем пустые строки

    def total_order_amount(self, obj):
        """
        Возвращает общую сумму всех товаров в заказе.
        """
        total = sum(item.price * item.quantity for item in obj.items.all())
        return f"{total:.2f} ₼"

    total_order_amount.short_description = "Ümumi məbləğ"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city', 'status', 'paid',
        'created_at', 'updated_at'
    ]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sales_chart_url'] = reverse('orders:sales_chart')
        return super().changelist_view(request, extra_context=extra_context)

    list_filter = ['paid', 'created_at', 'updated_at']
    list_display_links = ['id', 'first_name', 'last_name']
    inlines = [OrderItemInline]

    fieldsets = [
        ('Sifariş Məlumatı', {  # Название секции вместо "General"
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'address',
                'city',
                'country',
                'postal_code',
            )
        }),
        ('Status və Ödəniş', {  # Секция для статуса и оплаты
            'fields': ('status', 'paid', 'created_at', 'updated_at')
        }),
    ]

    readonly_fields = ('created_at', 'updated_at')  # Поля только для чтения

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Получаем объект заказа
        order = self.get_object(request, object_id)
        if order:
            # Вычисляем общую сумму
            total_amount = sum(item.price * item.quantity for item in order.items.all())
            extra_context = extra_context or {}
            extra_context['total_amount'] = f"{total_amount:.2f} ₼"
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    @admin.action(description='Отметить как отправленный')
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')

    @admin.action(description='Отметить как доставленный')
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
