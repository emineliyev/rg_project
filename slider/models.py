# 1. Django и сторонние библиотеки
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# 2. Импорты из проекта
from shop.models import Product


class Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sliders', verbose_name='Məhsul')
    title = models.CharField(max_length=100, verbose_name="Başlıq")
    description = models.TextField(verbose_name="Təsvir")
    image = models.ImageField(upload_to="slider", verbose_name='Şəkil')
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Slayder'
        verbose_name_plural = 'Slayderlər'


# SIGNALS
@receiver(post_delete, sender=Slider)
def delete_slider_image(sender, instance, **kwargs):
    if instance.image:
        default_storage.delete(instance.image.name)
