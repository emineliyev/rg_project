# Generated by Django 5.1.4 on 2025-01-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='E-poçt')),
            ],
            options={
                'verbose_name': 'E-poçt',
                'verbose_name_plural': 'E-poçtlar',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, verbose_name='Telefon')),
            ],
            options={
                'verbose_name': 'Telefon',
                'verbose_name_plural': 'Telefonlar',
            },
        ),
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ['-id'], 'verbose_name': 'Xüsusiyyət', 'verbose_name_plural': 'Xüsusiyyətlər'},
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='')),
                ('email', models.ManyToManyField(to='parameters.email', verbose_name='E-poçt')),
                ('phone', models.ManyToManyField(to='parameters.phone', verbose_name='Telefon')),
            ],
            options={
                'verbose_name': 'Əlaqə mməluamtı',
                'verbose_name_plural': 'Əlaqəmməluamtları',
            },
        ),
    ]
