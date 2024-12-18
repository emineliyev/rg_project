from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Səbət işə salınır. Məlumat sessiyada saxlanılır.
        """
        """
        Инициализация корзины. Данные хранятся в сессии.
        """
        """
        Initializing the basket. Data is stored in the session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Если корзина пуста, создаём пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, weight_option=None, quantity=1, override_quantity=False):
        """
        Səbətə məhsul əlavə edir və ya onun miqdarını yeniləyir.
        """
        """
        Добавляет продукт в корзину или обновляет его количество.
        """
        """
        Adds a product to the cart or updates its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'quantity': 0,
                'base_price': str(product.discounted_price),  # Базовая цена товара
                'weight_option': None
            }
        # Çəki parametrlərini və onun dəyişdiricisini təyin edir
        # Устанавливает параметры веса и его модификатор
        # Sets the weight parameters and its modifier
        if weight_option:
            self.cart[product_id]['weight_option'] = {
                'id': weight_option.id,
                'weight': str(weight_option.weight),
                'price_modifier': str(weight_option.price_modifier)
            }
        # Son qiyməti təyin edir (əsas qiymət + dəyişdirici)
        # Устанавливает итоговую цену (базовая цена + модификатор)
        # Sets the final price (base price + modifier)
        if weight_option:
            total_price = Decimal(product.discounted_price) + Decimal(weight_option.price_modifier)
        else:
            total_price = Decimal(product.discounted_price)

        self.cart[product_id]['price'] = str(total_price)  # Сохраняем финальную цену с учетом веса

        # Miqdarı yeniləyir
        # Обновляет количество
        # Updates the quantity
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Сохраняет изменения в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, weight_option=None):
        """
        Məhsulu səbətdən çıxarır.
        """
        """
        Удаляет продукт из корзины.
        """
        """
        Removes the product from the cart.
        """
        product_id = str(product.id)
        key = product_id
        if weight_option:
            key = f"{product_id}_{weight_option.id}"

        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        """
        Zibil qutusunu təmizləyir.
        """
        """
        Очищает корзину.
        """
        """
        Empties the Recycle Bin.
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        """
        Səbətdəki məhsulların ümumi dəyərini hesablayır.
        """
        """
        Рассчитывает общую стоимость товаров в корзине.
        """
        """
        Calculates the total cost of items in the cart.
        """
        total = Decimal(0)
        for item in self.cart.values():
            price = Decimal(item['price'])
            total += price * item['quantity']
        return total

    def __iter__(self):
        """
        Modeldən məlumat əlavə edərək səbətdəki elementləri döndərir.
        """
        """
        Итерация по товарам в корзине, добавляя данные из модели.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product
            cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
            yield cart_item

    def __len__(self):
        """
        Səbətdəki məhsulların ümumi sayını təmizləyir.
        """
        """
        Подчищает общее количество товаров в корзине.
        """
        """
        Clears the total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
