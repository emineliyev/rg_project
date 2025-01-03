from core import settings
from shop.models import Product


class Wishlist:
    def __init__(self, request):
        """
        Инициализация списка желаний. Данные хранятся в сессии.
        """
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def add(self, product):
        """
        Добавляет товар в список желаний.
        """
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {
                'name': product.name,
                'price': str(product.discounted_price),
                'image': product.images.first().image.url if product.images.exists() else None,
                'quantity': 1  # По умолчанию 1
            }
        self.save()

    def save(self):
        """
        Сохраняет изменения в сессии.
        """
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
        self.session.modified = True

    def remove(self, product):
        """
        Удаляет товар из списка желаний.
        """
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def clear(self):
        """
        Очищает список желаний.
        """
        self.session[settings.WISHLIST_SESSION_ID] = {}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            wishlist_item = self.wishlist[str(product.id)]
            yield {
                'id': product.id,
                'name': product.name,
                'price': wishlist_item['price'],
                'image': wishlist_item['image'],
                'quantity': wishlist_item['quantity']
            }

    def __len__(self):
        """
        Возвращает общее количество товаров в списке желаний.
        """
        return len(self.wishlist)
