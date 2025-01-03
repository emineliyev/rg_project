from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['display_weight', 'display_discount', 'display_discounted_price', 'display_original_price']  # Добавляем поле для отображения

    def display_weight(self, obj):
        """
        Отображает выбранный вес, если он есть.
        """
        if obj.weight_option:
            return f"{obj.weight_option.weight} q"
        return "N/A"

    display_weight.short_description = "Seşilən çəki"

    def display_discount(self, obj):
        """
        Отображает скидку на продукт.
        """
        if obj.product.discount > 0:
            return f"{obj.product.discount} %"
        return "Endirim yoxdur"

    display_discount.short_description = "Endirim"

    def display_discounted_price(self, obj):
        """
        Отображает цену со скидкой.
        """
        return f"{obj.product.discounted_price} ₼"

    display_discounted_price.short_description = "Endirimli qiymət"

    def display_original_price(self, obj):
        """
        Отображает цену без скидки.
        """
        return f"{obj.product.price} ₼"

    display_original_price.short_description = "Endirimsiz qiymət"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'status', 'paid',
                    'created_at', 'updated_at']
    list_filter = ['paid', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    @admin.action(description='Отметить как отправленный')
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')

    @admin.action(description='Отметить как доставленный')
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')

