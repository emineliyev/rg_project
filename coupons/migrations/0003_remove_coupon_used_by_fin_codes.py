# Generated by Django 5.1.4 on 2025-01-20 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_coupon_used_by_fin_codes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='used_by_fin_codes',
        ),
    ]
