from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from shop.models import Product, Image, SuperSale
from django.dispatch import receiver
from django.core.files.storage import default_storage
from slider.models import Slider


@receiver(post_delete, sender=Product)
def delete_product_video(sender, instance, **kwargs):
    if instance.video:
        default_storage.delete(instance.video.name)


@receiver(post_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    """
    Удаляет все изображения продукта после его удаления.
    """
    for image in instance.images.all():
        if image.image and default_storage.exists(image.image.name):
            default_storage.delete(image.image.name)


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    """
    Удаляет файл изображения после удаления записи Image.
    """
    if instance.image and default_storage.exists(instance.image.name):
        default_storage.delete(instance.image.name)


@receiver(post_save, sender=SuperSale)
def clear_super_sales_cache(sender, instance, **kwargs):
    cache.clear()


@receiver(post_save, sender=Slider)
def clear_slider_cache(sender, instance, **kwargs):
    cache.clear()