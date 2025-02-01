from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_photo')

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50"')

    get_photo.short_description = 'Şəkil'


