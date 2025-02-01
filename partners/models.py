from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad")
    image = models.ImageField(upload_to='partners/', verbose_name="Şəkil")
    url = models.URLField(verbose_name='Keçid')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tərəfdaş'
        verbose_name_plural = 'Tərəfdaşlar'
        ordering = ['name']