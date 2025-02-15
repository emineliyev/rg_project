from django.db import models
from tinymce.models import HTMLField


class Feature(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlıq")
    image = models.ImageField(upload_to='feature/', verbose_name="Şəkil")
    description = HTMLField(verbose_name="Təsvir")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Xüsusiyyət'
        verbose_name_plural = '8. Xüsusiyyətlər'
        ordering = ['-id']


class Phone(models.Model):
    number = models.CharField(max_length=20, verbose_name='Telefon')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Telefon'
        verbose_name_plural = '2. Telefonlar'


class Email(models.Model):
    email = models.EmailField(verbose_name='E-poçt')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'E-poçt'
        verbose_name_plural = '3. E-poçtlar'


class Contact(models.Model):
    address = models.TextField(verbose_name='Ünvan')
    phone = models.ManyToManyField(Phone, verbose_name='Telefon')
    email = models.ManyToManyField(Email, verbose_name='E-poçt')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Əlaqə mməluamtı'
        verbose_name_plural = '1. Əlaqə məluamtları'


class BaseContent(models.Model):
    title = models.CharField(max_length=250, verbose_name='Başlıq')
    description = HTMLField(verbose_name='Təsvir')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Yazılma tarixi')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class PrivacyPolicy(BaseContent):
    class Meta:
        verbose_name = 'Məxfilik Siyasəti'
        verbose_name_plural = '5. Məxfilik Siyasəti'


class DeliveryInformation(BaseContent):
    class Meta:
        verbose_name = 'Çatdırılma məlumatı'
        verbose_name_plural = '6. Çatdırılma məlumatı'


class ReturnsAndRefunds(BaseContent):
    class Meta:
        verbose_name = 'Qaytarmalar və Geri Ödənişlər'
        verbose_name_plural = '7. Geri ödəniş'


class TermsAndConditions(BaseContent):
    class Meta:
        verbose_name = 'Qaydalar və Şərtlər'
        verbose_name_plural = '4. Qaydalar və Şərtlər'
