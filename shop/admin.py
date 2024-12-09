from django.contrib import admin
from .models import (
    Category,
    Material,
    Piercing,
    PiercingImage,
    PiercingWeightOption,
    DiscountCampaign,
    PromoCode,
    Order,
    Notification,
    CartAnalytics,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Piercing)
class PiercingAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PiercingImage)
class PiercingImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PiercingWeightOption)
class PiercingWeightOptionAdmin(admin.ModelAdmin):
    list_display = ('piercing', 'weight', 'extra_price')


@admin.register(DiscountCampaign)
class DiscountCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'items')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message',)


@admin.register(CartAnalytics)
class CartAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user',)
