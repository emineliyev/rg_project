from django.db import models


class About(models.Model):
    title = models.CharField(max_length=100, default='Title', verbose_name='Başlıq')
    description = models.TextField(default='Description', verbose_name='Təsvir')
    image = models.ImageField(upload_to='about/%Y/%m/%d', null=True, blank=True, verbose_name='Şəkil')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Разрешает хранить только одну запись в базе"""
        if About.objects.exists() and not self.pk:
            raise ValueError("Можно создать только одну запись 'О нас'.")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'
