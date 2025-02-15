from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Account
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Kupon')
    valid_from = models.DateTimeField(verbose_name='Güvvəyə minir')
    valid_to = models.DateTimeField(verbose_name='Güvvədən düşür')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Güzəşt')
    active = models.BooleanField(default=True, verbose_name='Status')
    used_by_fin_codes = models.ManyToManyField(
        Account, blank=True, related_name='used_coupons', verbose_name='İstifadə edilmiş fin kodlar'
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Kupon'
        verbose_name_plural = 'Kuponlar'
