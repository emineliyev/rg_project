from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category, Material, Image, WeightOption, Comment


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
        'quantity_in_stock', 'weight_options_display', 'is_in_stock', 'product_rating', 'display_image'
    )
    list_editable = ('price', 'discount', 'quantity_in_stock')
    list_filter = ('category', 'material')
    search_fields = ('name', 'article')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline, WeightOptionInline]

    @admin.display(description='Изображение')
    def display_image(self, obj):
        # Отображаем первое изображение из связанных
        first_image = obj.images.first()
        if first_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>',
                               first_image.image.url)
        return "Нет изображения"

    @admin.display(description='Endirimli qiymət')
    def discounted_price(self, obj):
        return obj.discounted_price

    @admin.display(description='Reytinq')
    def product_rating(self, obj):
        return round(obj.average_rating(), 1)  # Округляем до 1 десятичного знака

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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rating')
    list_filter = ('rating',)
