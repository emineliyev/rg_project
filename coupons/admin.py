from django.contrib import admin
from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'valid_from', 'valid_to', 'discount', 'active')
    list_display_links = ('id', 'code')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('id', 'code')

