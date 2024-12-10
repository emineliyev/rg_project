from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ad')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slaq')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kateqoriyalar'


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ad')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slaq')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiallar'


def validate_discount(value):
    """Валидатор для скидки, проверяет, чтобы она была в диапазоне от 0 до 100."""
    """Endirim üçün Validator, onun 0-dan 100-ə qədər diapazonda olduğunu yoxlayır."""
    """A validator for the discount, checks that it is in the range from 0 to 100."""
    if not (0 <= value <= 100):
        raise ValidationError('Endirim 0-100 aralığında olmalıdır.')


class Product(models.Model):
    article = models.CharField(max_length=20, verbose_name='Artikul')
    name = models.CharField(max_length=60, verbose_name='Ad')
    slug = models.SlugField(max_length=60, unique=True, verbose_name='Slaq')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Kateqoriya')
    material = models.ForeignKey('Material', on_delete=models.CASCADE, verbose_name='Material')
    description = models.TextField(verbose_name='Təsvir')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Qiymət')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[validate_discount],
                                   verbose_name='Endirim (%)')
    quantity_in_stock = models.PositiveSmallIntegerField(
        verbose_name='Stokda olan miqdar')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə edilib')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənib')

    @property
    def discounted_price(self):
        """
        Рассчитывает цену со скидкой.
        Если скидка не установлена, возвращает полную цену.
        """
        """
        Endirimli qiyməti hesablayır.
        Endirim təyin olunmursa, tam qiyməti qaytarır.
        """
        """
        Calculates the discounted price.
        If no discount is set, returns the full price.
        """
        if self.discount > 0:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price

    @property
    def discount_amount(self):
        """
        Возвращает размер скидки в денежном выражении.
        """
        """
        Endirim məbləğini pul ifadəsində qaytarır.
        """
        """
        Returns the discount amount in monetary terms.
        """
        return round(self.price - self.discounted_price, 2)

    @property
    def is_in_stock(self):
        """
        Проверяет, есть ли товар в наличии.
        """
        """
        Məhsulun anbarda olub-olmadığını yoxlayır.
        """
        """
        Checks if the item is in stock.
        """
        return self.quantity_in_stock > 0

    def clean(self):
        """
        Дополнительная валидация модели.
        Убедимся, что скидка и цена согласованы.
        """
        """
        Əlavə model təsdiqi.
        Endirim və qiymətin razılaşdırıldığına əmin olaq.
        """
        """
        Additional model validation.
        Make sure the discount and price are consistent.
        """
        if self.price <= 0:
            raise ValidationError('Qiymət 0-dan böyük olmalıdır.')

    def __str__(self):
        return f"{self.name} ({self.article})"

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='')
    image = models.ImageField(upload_to='images/', verbose_name='')

    def __str__(self):
        return f"{self.product.name} - {self.product.article} Məhsul üçün şəkil"
