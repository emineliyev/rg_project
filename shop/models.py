from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''



