# Generated by Django 5.1.6 on 2025-02-11 20:17

import django.db.models.deletion
import mptt.fields
import shop.models
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ad')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slaq')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiallar',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ad')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slaq')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category')),
            ],
            options={
                'verbose_name': 'Kateqoriya',
                'verbose_name_plural': 'Kateqoriyalar',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(max_length=20, verbose_name='Artikul')),
                ('name', models.CharField(max_length=60, verbose_name='Ad')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='Slaq')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/', verbose_name='Видео файл')),
                ('description', tinymce.models.HTMLField(verbose_name='Təsvir')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qiymət')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[shop.models.validate_discount], verbose_name='Endirim (%)')),
                ('quantity_in_stock', models.PositiveSmallIntegerField(verbose_name='Stokda olan miqdar')),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='Populyarlıq')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Əlavə edilib')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Yenilənib')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Kateqoriya')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.material', verbose_name='Material')),
            ],
            options={
                'verbose_name': 'Məhsul',
                'verbose_name_plural': 'Məhsullar',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/', verbose_name='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60, verbose_name='Ad')),
                ('last_name', models.CharField(max_length=60, verbose_name='Soyad')),
                ('text', models.TextField(verbose_name='Şərh')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Tarix')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, verbose_name='Reytinq')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.product', verbose_name='Məhsul')),
            ],
            options={
                'verbose_name': 'Şərh',
                'verbose_name_plural': 'Şərhlər',
            },
        ),
        migrations.CreateModel(
            name='SuperSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', tinymce.models.HTMLField(verbose_name='Başlıq')),
                ('sale_date', models.DateField(verbose_name='Endirim tarixi')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Əlavə tarxi')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supersales', to='shop.product', verbose_name='Məhsul')),
            ],
            options={
                'verbose_name': 'Kompaniya',
                'verbose_name_plural': 'Kompaniya',
            },
        ),
        migrations.CreateModel(
            name='WeightOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Çəki (q)')),
                ('carat', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Karat')),
                ('size', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Ölçü (mm)')),
                ('price_modifier', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Çəkiyə görə qiymət')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weight_options', to='shop.product', verbose_name='Məhsul')),
            ],
            options={
                'verbose_name': 'Çəki seçimi',
                'verbose_name_plural': 'Çəki seçimləri',
            },
        ),
    ]
