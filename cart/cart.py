from decimal import Decimal
from django.conf import settings
from cart.forms import CartAddProductForm
from coupons.models import Coupon
from shop.models import Product

# ИЗМЕНИЛСЯ 06,02,2025
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
        self.coupon_id = self.session.get('coupon_id')
        self._cached_coupon = None  # ✅ Добавляем кеширование купона

    def add(self, product, weight_option=None, quantity=1, override_quantity=False):
        """
        Добавляет продукт в корзину или обновляет его количество.
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
        Удаляет продукт из корзины.
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
        Очищает корзину.
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        """
        Рассчитывает общую стоимость товаров в корзине.
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
            quantity = cart_item.get('quantity', 0)
            yield {
                'id': product.id,
                'name': product.name,
                'price': Decimal(cart_item['price']),
                'quantity': quantity,
                'total_price': Decimal(cart_item['price']) * quantity,
                'weight_option': cart_item.get('weight_option'),
                'product': product,
                'update_quantity_form': CartAddProductForm(initial={
                    'quantity': quantity,
                    'override': True
                })
            }

    def __len__(self):
        """
        Подчищает общее количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        """ ✅ Оптимизированный метод получения купона. """
        if self._cached_coupon is None and self.coupon_id:
            try:
                self._cached_coupon = Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                self._cached_coupon = None  # Если купона нет, не делаем новые запросы
        return self._cached_coupon

    def get_discount(self):
        """ ✅ Используем кешированный купон, чтобы не делать лишних SQL-запросов. """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """ ✅ Оптимизированный расчет стоимости со скидкой. """
        return self.get_total_price() - self.get_discount()
