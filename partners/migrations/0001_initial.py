# Generated by Django 5.1.4 on 2025-01-10 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ad')),
                ('image', models.ImageField(upload_to='partners/', verbose_name='Şəkil')),
            ],
            options={
                'verbose_name': 'Tərəfdaş',
                'verbose_name_plural': 'Tərəfdaşlar',
                'ordering': ['name'],
            },
        ),
    ]
