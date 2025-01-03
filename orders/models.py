from django.contrib.admin.models import LogEntry, ADDITION
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from core import settings
from shop.models import Product, WeightOption


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Emal gözlənilir'),
        ('PROCESSING', 'Emal edilir'),
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
    email = models.EmailField(verbose_name='E=poçt')
    country = models.CharField(max_length=50, verbose_name='Ölkə')
    city = models.CharField(max_length=50, verbose_name='Bölgə')
    address = models.CharField(max_length=100, verbose_name='Ünvan')
    postal_code = models.CharField(max_length=50, verbose_name='Poçt kodu')
    phone_number = models.CharField(max_length=50, verbose_name='Telefon')
    status = models.CharField(
        max_length=23,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Çatdırılma statusu'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sifariş tarixi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')
    paid = models.BooleanField(default=False, verbose_name='Ödənilib')

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Sifariş'
        verbose_name_plural = 'Sifarişlər'

    def get_total(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Məhsul')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Alınan qiymət')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Miqdar')
    weight_option = models.ForeignKey(
        WeightOption, null=True, blank=True, on_delete=models.SET_NULL, related_name='order_items',
        verbose_name='Выбранный вес'
    )  # Поле для хранения выбранного веса

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity
