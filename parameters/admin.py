from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Feature, Email, Phone, Contact, PrivacyPolicy, DeliveryInformation, ReturnsAndRefunds, \
    TermsAndConditions


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_photo')

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50"')

    get_photo.short_description = 'Şəkil'


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at')


@admin.register(DeliveryInformation)
class DeliveryInformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at')


@admin.register(ReturnsAndRefunds)
class ReturnsAndRefundsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at')


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at')
