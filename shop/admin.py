from django.contrib import admin
from .models import Product, Category, Material, Image, WeightOption


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class WeightOptionInline(admin.TabularInline):
    model = WeightOption
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
        'quantity_in_stock', 'weight_options_display', 'is_in_stock'
    )
    list_editable = ('price', 'discount', 'quantity_in_stock')
    list_filter = ('category', 'material')
    search_fields = ('name', 'article')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline, WeightOptionInline]

    @admin.display(description='Endirimli qiymət')
    def discounted_price(self, obj):
        return obj.discounted_price

    @admin.display(description='Endirim məbləği')
    def discount_amount(self, obj):
        return obj.discount_amount

    @admin.display(description='Stokda var')
    def is_in_stock(self, obj):
        return "Var" if obj.is_in_stock else "Yoxdur"

    @admin.display(description="Çəki seçimləri")
    def weight_options_display(self, obj):
        """
        Отображает все опции веса и их модификаторы цен для продукта.
        """
        """
        Məhsul üçün bütün çəki seçimlərini və onların qiymət dəyişdiricilərini göstərir.
        """
        """
        Displays all weight options and their price modifiers for the product.
        """
        options = obj.weight_options.all()
        if options.exists():
            return ", ".join(
                [f"{opt.weight} г (+{opt.price_modifier}₼)" for opt in options]
            )
        return "Seçim yoxdur"
