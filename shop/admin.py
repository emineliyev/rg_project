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


class PiercingImageInline(admin.TabularInline):
    model = PiercingImage
    extra = 1

@admin.register(Piercing)
class PiercingAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PiercingImageInline]

    def main_image_preview(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image and main_image.images:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', main_image.images.url)
        return "No image"

    main_image_preview.short_description = "Главная картинка"


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
