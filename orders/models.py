# 1. Встроенные библиотеки Python
from decimal import Decimal

# 2. Django и сторонние библиотеки
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

# 3. Импорты из проекта
from core import settings
from coupons.models import Coupon
from shop.models import Product, WeightOption


class Order(models.Model):
    """
    Модель заказа
    """
    STATUS_CHOICES = [
        ('PENDING', 'Sifarişiniz alındı'),
        ('PROCESSING', 'Sifarişiniz hazırlanır'),
        ('SHIPPED', 'Göndərilib'),
        ('IN_TRANSIT', 'Yoldadır'),
        ('DELIVERED', 'Çatdırıldı'),
        ('CANCELLED', 'Ləğv edildi'),
        ('RETURNED', 'Qaytarıldı'),
        ('FAILED', 'Çatdırılma uğursuz oldu'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True,
                             blank=True, verbose_name='İstifadəçi')
    first_name = models.CharField(max_length=60, verbose_name='Ad')
    last_name = models.CharField(max_length=60, verbose_name='Soyad')
    fin_code = models.CharField(max_length=7, verbose_name='Fin kod')
    email = models.EmailField(verbose_name='E-poçt')
    country = models.CharField(max_length=50, verbose_name='Ölkə')
    city = models.CharField(max_length=50, verbose_name='Bölgə')
    address = models.CharField(max_length=100, verbose_name='Ünvan')
    postal_code = models.CharField(max_length=50, verbose_name='Poçt kodu')
    phone_number = models.CharField(max_length=50, verbose_name='Telefon')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Cəmi məbləğ (güzəştdən sonra)"
    )
    status = models.CharField(
        max_length=23,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Çatdırılma statusu'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sifariş tarixi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')
    paid = models.BooleanField(default=False, verbose_name='Ödəniş statusu')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kupon',
                               related_name='orders')
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Discount')

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Sifariş'
        verbose_name_plural = 'Sifarişlər'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    @staticmethod
    def get_sales_data():
        sales = (
            Order.objects.filter(status='DELIVERED')
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total_sales=Sum('total_price'))
            .order_by('month')
        )
        return sales


class OrderItem(models.Model):
    """
    Модель элемента заказа
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Məhsul')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Alınan qiymət')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Miqdar')
    weight_option = models.ForeignKey(
        WeightOption, null=True, blank=True, on_delete=models.SET_NULL, related_name='order_items',
        verbose_name='Seçilmiş çəki'
    )  # Поле для хранения выбранного веса

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity
