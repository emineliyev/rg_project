from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now


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
    video = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name='Видео файл')
    description = models.TextField(verbose_name='Təsvir')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Qiymət')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[validate_discount],
                                   verbose_name='Endirim (%)')
    quantity_in_stock = models.PositiveSmallIntegerField(
        verbose_name='Stokda olan miqdar')
    popularity = models.PositiveIntegerField(default=0, verbose_name="Популярность")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə edilib')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənib')

    def average_rating(self):
        comments = self.comments.all()
        if comments.exists():
            return sum(comment.rating for comment in comments) / comments.count()
        return 0

    # def get_absolute_url(self):
    #     return reverse('product_detail', kwargs={'slug': self.slug})

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

    def __str__(self):
        return f"{self.name} ({self.article})"

    @property
    def is_new(self):
        """
        Проверяет, является ли товар новым (например, добавлен в последние 30 дней).
        """
        return now() - self.create_at <= timedelta(days=30)

    @property
    def is_popular(self):
        """
        Проверяет, является ли товар популярным (например, имеет популярность выше 100).
        """
        return self.popularity > 100

    class Meta:
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'


class WeightOption(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='weight_options', verbose_name='Məhsul'
    )
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Çəki (q)')
    carat = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Karat')
    size = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Ölçü (mm)')
    price_modifier = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Çəkiyə görə qiymət'
    )

    def __str__(self):
        return f"{self.product.name} - {self.weight}q (+{self.price_modifier}₼)"

    class Meta:
        verbose_name = 'Çəki seçimi'
        verbose_name_plural = 'Çəki seçimləri'


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='')
    image = models.ImageField(upload_to='images/', verbose_name='')

    def __str__(self):
        return f"{self.product.name} - {self.product.article} Məhsulu üçün şəkil"


class SuperSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supersales', verbose_name='')
    title = models.CharField(max_length=255, verbose_name='Başlıq')
    days = models.PositiveSmallIntegerField(verbose_name='Gün')
    hours = models.PositiveSmallIntegerField(verbose_name='Saat')
    minutes = models.PositiveSmallIntegerField(verbose_name='Dəqiqə')
    seconds = models.PositiveSmallIntegerField(verbose_name='Saniyə')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə tarxi')

    def __str__(self):
        return f"{self.product.name} - {self.title}"

    class Meta:
        verbose_name = 'Kompaniya'
        verbose_name_plural = 'Kompaniya'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Məhsul')
    first_name = models.CharField(max_length=60, verbose_name='Ad')
    last_name = models.CharField(max_length=60, verbose_name='Soyad')
    text = models.TextField(verbose_name='Şərh')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarix')
    rating = models.PositiveSmallIntegerField(
        verbose_name='Reytinq',
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product.name} ({self.rating})"

    class Meta:
        verbose_name = 'Şərh'
        verbose_name_plural = 'Şərhlər'

