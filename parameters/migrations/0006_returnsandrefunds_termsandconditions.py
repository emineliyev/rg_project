# Generated by Django 5.1.4 on 2025-01-12 18:45

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0005_deliveryinformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnsAndRefunds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Başlıq')),
                ('description', tinymce.models.HTMLField(verbose_name='Təsvir')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Yazılma tarixi')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')),
            ],
            options={
                'verbose_name': 'Qaytarmalar və Geri Ödənişlər',
                'verbose_name_plural': 'Qaytarmalar və Geri Ödənişlər',
            },
        ),
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Başlıq')),
                ('description', tinymce.models.HTMLField(verbose_name='Təsvir')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Yazılma tarixi')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')),
            ],
            options={
                'verbose_name': 'Qaydalar və Şərtlər',
                'verbose_name_plural': 'Qaydalar və Şərtlər',
            },
        ),
    ]
