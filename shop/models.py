from django.db import models
from django.utils import timezone

class DiscountCampaign(models.Model):
    """
    Модель для представления акций, которые применяются к пирсингам
    в заданный период времени.
    """
    name = models.CharField(max_length=255, verbose_name="Название акции")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент скидки",
        help_text="Процент скидки, который будет применен (например, 10 для 10%)."
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def is_valid(self):
        """
        Проверяет, активна ли акция в данный момент.
        """
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}% скидка)"


class Piercing(models.Model):
    """
    Модель для представления пирсингов и их базовых характеристик.
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, verbose_name="Тип")
    material = models.CharField(max_length=100, verbose_name="Материал")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    body_part = models.CharField(max_length=100, verbose_name="Часть тела")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="piercings/", blank=True, null=True, verbose_name="Изображение")
    in_stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    is_active = models.BooleanField(default=True, verbose_name="Активен для продажи")
    campaigns = models.ManyToManyField(
        DiscountCampaign,
        blank=True,
        related_name="piercings",
        verbose_name="Акции"
    )

    def get_discounted_price(self):
        """
        Возвращает цену со скидкой, если активные акции есть.
        Если скидок нет, возвращается базовая цена.
        """
        active_campaigns = self.campaigns.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        if active_campaigns.exists():
            max_discount = max(campaign.discount_percentage for campaign in active_campaigns)
            return self.base_price * (1 - max_discount / 100)
        return self.base_price

    def __str__(self):
        return self.name


class PiercingWeightOption(models.Model):
    """
    Модель для представления вариаций пирсингов по весу с дополнительной ценой.
    """
    piercing = models.ForeignKey(Piercing, related_name='weight_options', on_delete=models.CASCADE, verbose_name="Пирсинг")
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Вес (г)")
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Дополнительная цена")

    def __str__(self):
        return f"{self.piercing.name} - {self.weight} г"


class CartItem(models.Model):
    """
    Модель для представления отдельного товара в корзине.
    """
    piercing = models.ForeignKey(Piercing, on_delete=models.CASCADE, verbose_name="Пирсинг")
    weight_option = models.ForeignKey(PiercingWeightOption, on_delete=models.CASCADE, verbose_name="Весовая опция", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def get_price(self):
        """
        Рассчитывает цену товара с учетом выбранного веса и скидок.
        """
        base_price = self.piercing.get_discounted_price()
        extra_price = self.weight_option.extra_price if self.weight_option else 0
        return (base_price + extra_price) * self.quantity

    def __str__(self):
        return f"{self.piercing.name} - {self.quantity} шт."


class Cart(models.Model):
    """
    Модель для представления корзины покупателя.
    """
    items = models.ManyToManyField(CartItem, verbose_name="Товары")

    def get_total_price(self):
        """
        Рассчитывает итоговую сумму корзины с учетом скидок.
        """
        return sum(item.get_price() for item in self.items.all())

    def get_total_quantity(self):
        """
        Рассчитывает общее количество товаров в корзине.
        """
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Корзина ({self.get_total_quantity()} товаров)"
