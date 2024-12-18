from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Инициализация корзины. Данные хранятся в сессии.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Если корзина пуста, создаём пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, weight_option=None, quantity=1, override_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'quantity': 0,
                'base_price': str(product.discounted_price),  # Базовая цена товара
                'weight_option': None
            }

        # Устанавливаем параметры веса и его модификатор
        if weight_option:
            self.cart[product_id]['weight_option'] = {
                'id': weight_option.id,
                'weight': str(weight_option.weight),
                'price_modifier': str(weight_option.price_modifier)
            }

        # Устанавливаем итоговую цену (базовая цена + модификатор)
        if weight_option:
            total_price = Decimal(product.discounted_price) + Decimal(weight_option.price_modifier)
        else:
            total_price = Decimal(product.discounted_price)

        self.cart[product_id]['price'] = str(total_price)  # Сохраняем финальную цену с учетом веса

        # Обновляем количество
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
        Удалить продукт из корзины.
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
        Очистить корзину.
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        """
        Рассчитать общую стоимость товаров в корзине.
        """
        total = Decimal(0)
        for item in self.cart.values():
            price = Decimal(item['price'])
            total += price * item['quantity']
        return total

    def __iter__(self):
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
        Подсчитать общее количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())
