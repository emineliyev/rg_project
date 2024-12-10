from django.contrib import admin
from .models import Product, Category, Material, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'article', 'price', 'discount', 'discounted_price', 'discount_amount',
        'quantity_in_stock', 'is_in_stock'
    )
    list_editable = ('price', 'discount', 'quantity_in_stock')
    list_filter = ('category', 'material')
    search_fields = ('name', 'article')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline]

    @admin.display(description='Endirimli qiymət')
    def discounted_price(self, obj):
        return obj.discounted_price

    @admin.display(description='Endirim məbləği')
    def discount_amount(self, obj):
        return obj.discount_amount

    @admin.display(description='Stokda var')
    def is_in_stock(self, obj):
        return "Var" if obj.is_in_stock else "Yoxdur"
