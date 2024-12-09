from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Piercing(models.Model):
    """
    Модель для представления пирсингов.
    """
    code = models.CharField(max_length=60, verbose_name='Код')
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, max_length=255, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Материал')
    video = models.FileField(upload_to='video/%Y/%m/%d', verbose_name='Видео')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена")
    in_stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    discount_threshold = models.PositiveIntegerField(
        default=10, verbose_name="Порог для скидки",
        help_text="Количество товара, начиная с которого применяется скидка"
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name="Процент скидки",
        help_text="Процент скидки при покупке количества, равного или превышающего порог"
    )
    recommendations = models.ManyToManyField(
        'self',
        blank=True,
        related_name='recommended_for',
        verbose_name="Рекомендуемые товары"
    )
    campaigns = models.ManyToManyField(
        'DiscountCampaign',
        blank=True,
        related_name='piercings',
        verbose_name="Акции"
    )

    def get_discounted_price(self, quantity):
        """
        Рассчитывает цену с учетом скидок на количество и временных акций.
        """
        price = self.base_price

        # Применяем скидку на основе количества
        if quantity >= self.discount_threshold:
            price *= (1 - self.discount_percentage / 100)

        # Применяем максимальную скидку из активных акций
        active_campaigns = self.campaigns.filter(is_active=True, start_date__lte=now(), end_date__gte=now())
        if active_campaigns.exists():
            max_campaign_discount = max(campaign.discount_percentage for campaign in active_campaigns)
            price *= (1 - max_campaign_discount / 100)

        return price

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пирсинг'
        verbose_name_plural = 'Пирсинги'


class PiercingImage(models.Model):
    piercing = models.ForeignKey(Piercing, models.CASCADE, verbose_name='Пирсинг')
    images = models.ImageField(upload_to='piercing/%Y/%m/%d', verbose_name='Картинка')

    def __str__(self):
        return self.piercing.name

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'


class PiercingWeightOption(models.Model):
    """
    Модель для представления весовых вариаций пирсинга.
    """
    piercing = models.ForeignKey(Piercing, related_name='weight_options', on_delete=models.CASCADE,
                                 verbose_name="Пирсинг")
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Вес (г)")
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Дополнительная цена")

    def __str__(self):
        return f"{self.piercing.name} - {self.weight} г"

    class Meta:
        verbose_name = 'Вес'
        verbose_name_plural = 'Весы'


class DiscountCampaign(models.Model):
    """
    Модель для временных акций и скидок.
    """
    name = models.CharField(max_length=255, verbose_name="Название акции")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент скидки",
        help_text="Процент скидки, применяемый к товарам в рамках акции"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def is_valid(self):
        """
        Проверяет, активна ли акция в данный момент.
        """
        return self.is_active and self.start_date <= now() <= self.end_date

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}%)"

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class PromoCode(models.Model):
    """
    Модель для промокодов.
    """
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент скидки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    valid_from = models.DateTimeField(verbose_name="Начало действия")
    valid_to = models.DateTimeField(verbose_name="Окончание действия")

    def is_valid(self):
        """
        Проверка активности промокода.
        """
        return self.is_active and self.valid_from <= now() <= self.valid_to

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промо код'
        verbose_name_plural = 'Промо коды'


class Order(models.Model):
    """
    Модель для представления заказов.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    items = models.JSONField(default=dict, verbose_name="Список товаров")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Ожидает обработки'),
            ('completed', 'Завершён'),
            ('cancelled', 'Отменён'),
            ('returned', 'Возвращён')
        ],
        default='pending',
        verbose_name="Статус заказа"
    )

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username} ({self.status})"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Notification(models.Model):
    """
    Модель для уведомлений о снижении цен и доступности товара.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    def __str__(self):
        return f"Уведомление для {self.user.username}"

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'


class CartAnalytics(models.Model):
    """
    Модель для аналитики корзины.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_analytics", null=True, blank=True)
    cart_data = models.JSONField(default=dict, verbose_name="Данные корзины")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"Аналитика корзины ({self.created_at})"

    class Meta:
        verbose_name = 'Аналитика'
        verbose_name_plural = 'Аналитики'
