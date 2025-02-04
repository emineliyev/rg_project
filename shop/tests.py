from django.db.models import Max, Min
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta

from cart.forms import CartAddProductForm
from parameters.models import Feature, Contact
from partners.models import Partner
from shop.models import (
    Product, Category, Material, SuperSale,
    WeightOption, Image, Comment
)
from slider.models import Slider


# class HomeProductListViewTest(TestCase):
#     def setUp(self):
#         """Создаём тестовые данные"""
#         self.category = Category.objects.create(name="Test Category", slug="test-category")
#         self.material = Material.objects.create(name="Test Material", slug="test-material")
#         Contact.objects.create(
#             address="Тестовый адрес"
#         )
#
#         # Создаём 10 тестовых товаров
#         for i in range(10):
#             product = Product.objects.create(
#                 article=f"ART-{i}",
#                 name=f"Product {i}",
#                 slug=f"product-{i}",
#                 category=self.category,
#                 material=self.material,
#                 price=100.00 + i,
#                 discount=i * 5,
#                 quantity_in_stock=i + 1,  # Избегаем 0, чтобы `is_in_stock` работал
#                 popularity=i * 50,  # Первые товары будут более популярными
#                 create_at=now() - timedelta(days=i * 5),  # Каждый товар с разной датой создания
#             )
#
#             # Добавляем к каждому товару WeightOption и Image
#             WeightOption.objects.create(
#                 product=product, weight=10.0, carat=5.0, size=15.0, price_modifier=20.0
#             )
#             Image.objects.create(product=product, image="product/test.jpg")
#
#         # Берём первый созданный продукт
#         self.product = Product.objects.first()
#
#         # Создаём `Slider`
#         Slider.objects.create(
#             product=self.product,
#             title="Test Slider",
#             description="This is a test slider",
#             image="slider1.jpg",
#             status=True
#         )
#
#         # Создаём `SuperSale`
#         SuperSale.objects.create(
#             product=self.product,
#             title="<b>Big Sale!</b>",
#             sale_date=now().date(),
#             status=True
#         )
#
#         # Создаём партнёров и особенности (Feature)
#         Partner.objects.create(name="Partner 1", image="partner.jpg", url="https://partner.com")
#         Feature.objects.create(title="Feature 1", image="feature.jpg", description="Description")
#
#     def test_homepage_status_code(self):
#         """Проверяем, что главная страница открывается без ошибок"""
#         response = self.client.get(reverse("shop:index"))  # Убедись, что у тебя есть URL с name="home"
#         self.assertEqual(response.status_code, 200)
#
#     def test_homepage_context(self):
#         """Проверяем, что в контексте есть нужные данные"""
#         response = self.client.get(reverse("shop:index"))  # Если `app_name` нет
#         context = response.context
#
#         # Проверяем товары (должно быть 8 товаров)
#         self.assertIn("products", context)
#         self.assertEqual(len(context["products"]), 8)
#
#         # Проверяем `new_products` (созданные за последние 30 дней)
#         self.assertIn("new_products", context)
#         new_products = Product.objects.filter(create_at__gte=now() - timedelta(days=30))
#         self.assertEqual(len(context["new_products"]), min(8, new_products.count()))
#
#         # Проверяем `popular_products` (popularity > 100)
#         self.assertIn("popular_products", context)
#         popular_products = Product.objects.filter(popularity__gt=100)
#         self.assertEqual(len(context["popular_products"]), min(8, popular_products.count()))
#
#         # Проверяем слайдеры
#         self.assertIn("sliders", context)
#         self.assertEqual(len(context["sliders"]), 1)
#
#         # Проверяем супер-распродажу
#         self.assertIn("super_sales", context)
#         self.assertEqual(len(context["super_sales"]), 1)
#
#         # Проверяем партнёров
#         self.assertIn("partners", context)
#         self.assertGreaterEqual(len(context["partners"]), 1)
#
#         # Проверяем особенности (Feature)
#         self.assertIn("features", context)
#         self.assertGreaterEqual(len(context["features"]), 1)


# class ProductDetailViewTest(TestCase):
#     def setUp(self):
#         """Создаём тестовые данные"""
#         self.category = Category.objects.create(name="Test Category", slug="test-category")
#         self.material = Material.objects.create(name="Test Material", slug="test-material")
#
#         # Создаём тестовый продукт
#         self.product = Product.objects.create(
#             article="ART-001",
#             name="Test Product",
#             slug="test-product",
#             category=self.category,
#             material=self.material,
#             price=100.00,
#             discount=10,
#             quantity_in_stock=5,
#             popularity=150,
#             create_at=now() - timedelta(days=5),
#         )
#
#         # Создаём изображения и весовые опции
#         Image.objects.create(product=self.product, image="product/test.jpg")
#         WeightOption.objects.create(
#             product=self.product, weight=10.0, carat=5.0, size=15.0, price_modifier=20.0
#         )
#
#         # Создаём похожий товар (в той же категории)
#         self.related_product = Product.objects.create(
#             article="ART-002",
#             name="Related Product",
#             slug="related-product",
#             category=self.category,
#             material=self.material,
#             price=120.00,
#             discount=5,
#             quantity_in_stock=3,
#             popularity=90,
#             create_at=now() - timedelta(days=10),
#         )
#
#         # Создаём комментарий
#         self.comment = Comment.objects.create(
#             product=self.product,
#             first_name="Test",
#             last_name="User",
#             rating=4,
#             text="This is a test comment",
#         )
#
#     def test_product_detail_status_code(self):
#         """Проверяем, что страница продукта открывается без ошибок"""
#         response = self.client.get(reverse("shop:product_detail", kwargs={"slug": self.product.slug}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_detail_context(self):
#         """Проверяем, что в контексте передаются нужные данные"""
#         response = self.client.get(reverse("shop:product_detail", kwargs={"slug": self.product.slug}))
#         context = response.context
#
#         # Проверяем, что передаётся продукт
#         self.assertEqual(context["object"], self.product)
#
#         # Проверяем изображения и видео
#         self.assertIn("images", context)
#         self.assertEqual(len(context["images"]), 1)  # Должно быть 1 изображение
#
#         self.assertIn("video", context)
#         self.assertFalse(context["video"])  # Проверяем, что видео пустое
#
#         # Проверяем весовые опции
#         self.assertIn("weight_options", context)
#         self.assertEqual(len(context["weight_options"]), 1)  # Должна быть 1 весовая опция
#
#         # Проверяем форму корзины
#         self.assertIn("cart_product_form", context)
#         self.assertIsInstance(context["cart_product_form"], CartAddProductForm)
#
#         # Проверяем комментарии
#         self.assertIn("comments", context)
#         self.assertEqual(len(context["comments"]), 1)  # 1 комментарий
#
#         self.assertIn("comments_count", context)
#         self.assertEqual(context["comments_count"], 1)  # Должно быть 1 комментарий
#
#         # Проверяем похожие товары
#         self.assertIn("related_products", context)
#         self.assertEqual(len(context["related_products"]), 1)  # Должен быть 1 похожий товар
#
#     def test_post_comment_form_valid(self):
#         """Проверяем отправку комментария (POST-запрос)"""
#         data = {
#             "first_name": "New",
#             "last_name": "User",
#             "rating": 5,
#             "text": "This is another test comment",
#         }
#         response = self.client.post(
#             reverse("shop:product_detail", kwargs={"slug": self.product.slug}),
#             data
#         )
#
#         # Проверяем, что редиректит на ту же страницу
#         self.assertRedirects(response, reverse("shop:product_detail", kwargs={"slug": self.product.slug}))
#
#         # Проверяем, что комментарий добавился
#         self.assertEqual(Comment.objects.count(), 2)  # Был 1, теперь 2

# class BaseProductListViewTest(TestCase):
#     def setUp(self):
#         """Создаём тестовые данные"""
#         self.category = Category.objects.create(name="Test Category", slug="test-category")
#         self.material = Material.objects.create(name="Test Material", slug="test-material")
#
#         # Создаём 15 товаров для теста пагинации
#         for i in range(15):
#             Product.objects.create(
#                 article=f"ART-{i}",
#                 name=f"Product {i}",
#                 slug=f"product-{i}",
#                 category=self.category,
#                 material=self.material,
#                 price=50.0 + i * 10,  # Разные цены для тестов фильтрации
#                 discount=5,
#                 quantity_in_stock=5,
#                 popularity=i * 20,  # Разные уровни популярности
#                 create_at=now() - timedelta(days=i),
#             )
#
#         # Добавляем изображение к первому продукту
#         self.product = Product.objects.first()
#         Image.objects.create(product=self.product, image="product/test.jpg")
#
#     def test_product_list_status_code(self):
#         """Проверяем, что список товаров открывается без ошибок"""
#         response = self.client.get(reverse("shop:products"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_product_list_pagination(self):
#         """Проверяем, что работает пагинация (9 товаров на странице)"""
#         response = self.client.get(reverse("shop:products"))
#         context = response.context
#         self.assertEqual(len(context["products"]), 9)  # Должно быть 9 товаров на первой странице
#
#         # Проверяем вторую страницу
#         response = self.client.get(reverse("shop:products") + "?page=2")
#         self.assertEqual(len(response.context["products"]), 6)  # Оставшиеся 6 товаров
#
#     def test_filter_by_price(self):
#         """Проверяем фильтрацию по цене"""
#         response = self.client.get(reverse("shop:products") + "?price_min=70&price_max=120")
#         filtered_products = Product.objects.filter(price__gte=70, price__lte=120)
#         self.assertEqual(len(response.context["products"]), filtered_products.count())
#
#     def test_filter_by_search_query(self):
#         """Проверяем поиск по названию и описанию"""
#         response = self.client.get(reverse("shop:products") + "?q=Product 1")
#         filtered_products = Product.objects.filter(name__icontains="Product 1") | \
#                             Product.objects.filter(description__icontains="Product 1")
#         self.assertEqual(len(response.context["products"]), filtered_products.count())
#
#     def test_sorting(self):
#         """Проверяем сортировку"""
#         # По имени (A-Z)
#         response = self.client.get(reverse("shop:products") + "?sort=name")
#         sorted_products = Product.objects.order_by("name")[:9]
#         self.assertQuerySetEqual(response.context["products"], sorted_products, transform=lambda x: x)
#
#         # По цене (по возрастанию)
#         response = self.client.get(reverse("shop:products") + "?sort=price_asc")
#         sorted_products = Product.objects.order_by("price")[:9]
#         self.assertQuerySetEqual(response.context["products"], sorted_products, transform=lambda x: x)
#
#         # По цене (по убыванию)
#         response = self.client.get(reverse("shop:products") + "?sort=price_desc")
#         sorted_products = Product.objects.order_by("-price")[:9]
#         self.assertQuerySetEqual(response.context["products"], sorted_products, transform=lambda x: x)
#
#         # По новизне (последние добавленные)
#         response = self.client.get(reverse("shop:products") + "?sort=newest")
#         sorted_products = Product.objects.order_by("-create_at")[:9]
#         self.assertQuerySetEqual(response.context["products"], sorted_products, transform=lambda x: x)
#
#     def test_context_data(self):
#         """Проверяем, что в контексте передаются нужные данные"""
#         response = self.client.get(reverse("shop:products"))
#         context = response.context
#
#         # Проверяем категории
#         self.assertIn("categories", context)
#         self.assertEqual(len(context["categories"]), 1)
#
#         # Проверяем популярные товары
#         self.assertIn("popular_products", context)
#         popular_products = Product.objects.filter(popularity__gt=100)[:3]
#         self.assertEqual(len(context["popular_products"]), popular_products.count())
#
#         # Проверяем диапазон цен
#         self.assertIn("max_salary", context)
#         self.assertIn("min_salary", context)
#         price_range = Product.objects.aggregate(max_price=Max("price"), min_price=Min("price"))
#         self.assertEqual(context["max_salary"], price_range["max_price"])
#         self.assertEqual(context["min_salary"], price_range["min_price"])
#
#         # Проверяем общее количество товаров
#         self.assertIn("product_count", context)
#         self.assertEqual(context["product_count"], Product.objects.count())
#
#         self.assertIn("all_products", context)
#         self.assertEqual(context["all_products"], Product.objects.count())

# class CategoryProductListViewTest(TestCase):
#     def setUp(self):
#         """Создаём тестовые данные"""
#         self.parent_category = Category.objects.create(name="Parent Category", slug="parent-category")
#         self.child_category = Category.objects.create(name="Child Category", slug="child-category", parent=self.parent_category)
#
#         self.material = Material.objects.create(name="Test Material", slug="test-material")
#
#         # Создаём товары в разных категориях
#         for i in range(10):
#             Product.objects.create(
#                 article=f"ART-{i}",
#                 name=f"Product {i}",
#                 slug=f"product-{i}",
#                 category=self.parent_category if i < 5 else self.child_category,
#                 material=self.material,
#                 price=50.0 + i * 10,
#                 discount=5,
#                 quantity_in_stock=5,
#                 popularity=i * 20,
#                 create_at=now() - timedelta(days=i),
#             )
#
#         # Добавляем изображение к первому продукту
#         self.product = Product.objects.first()
#         Image.objects.create(product=self.product, image="product/test.jpg")
#
#     def test_category_product_list_status_code(self):
#         """Проверяем, что страница категории открывается без ошибок"""
#         response = self.client.get(reverse("shop:category", kwargs={"slug": self.parent_category.slug}))
#         self.assertEqual(response.status_code, 200)
#
#     def test_filter_by_category(self):
#         """Проверяем, что выводятся только товары из нужной категории"""
#         response = self.client.get(reverse("shop:category", kwargs={"slug": self.parent_category.slug}))
#
#         filtered_products = Product.objects.filter(category__in=self.parent_category.get_descendants(include_self=True))
#
#         # Проверяем, что в QuerySet попали только нужные товары, НО без учёта пагинации
#         self.assertEqual(response.context["product_count"], filtered_products.count())
#
#     def test_context_current_category(self):
#         """Проверяем, что в контексте передаётся текущая категория"""
#         response = self.client.get(reverse("shop:category", kwargs={"slug": self.child_category.slug}))
#         context = response.context
#         self.assertIn("current_category", context)
#         self.assertEqual(context["current_category"], self.child_category)
#
#     def test_category_product_list_pagination(self):
#         """Проверяем, что работает пагинация"""
#         response = self.client.get(reverse("shop:category", kwargs={"slug": self.parent_category.slug}))
#         self.assertEqual(len(response.context["products"]), min(9, Product.objects.count()))
#
#     def test_search_in_category(self):
#         """Проверяем поиск по названию внутри категории"""
#         response = self.client.get(reverse("shop:category", kwargs={"slug": self.parent_category.slug}) + "?q=Product 1")
#         filtered_products = Product.objects.filter(
#             category__in=self.parent_category.get_descendants(include_self=True),
#             name__icontains="Product 1"
#         )
#         self.assertEqual(len(response.context["products"]), filtered_products.count())
#
#     def test_sorting_in_category(self):
#         """Проверяем сортировку товаров внутри категории"""
#         response = self.client.get(reverse("shop:category", kwargs={"slug": self.parent_category.slug}) + "?sort=price_desc")
#         sorted_products = Product.objects.filter(category__in=self.parent_category.get_descendants(include_self=True)).order_by("-price")[:9]
#         self.assertQuerySetEqual(response.context["products"], sorted_products, transform=lambda x: x)