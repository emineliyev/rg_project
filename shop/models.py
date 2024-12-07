from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name='')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''


class Piercing(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    type = models.CharField(max_length=100, verbose_name="Тип")
    material = models.CharField(max_length=100, verbose_name="Материал")
    size = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Размер (мм)")
    gauge = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Толщина (мм)")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    coating = models.CharField(max_length=100, blank=True, null=True, verbose_name="Покрытие")
    inserts = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вставки")
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Вес (г)")
    hypoallergenic = models.BooleanField(default=False, verbose_name="Гипоаллергенность")
    body_part = models.CharField(max_length=100, verbose_name="Часть тела")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="piercings/", blank=True, null=True, verbose_name="Изображение")
    in_stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    is_active = models.BooleanField(default=True, verbose_name="Активно для продажи")

    def __str__(self):
        return self.name
