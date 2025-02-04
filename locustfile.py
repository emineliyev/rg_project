from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8000"  # Указываем адрес Django-сервера
    wait_time = between(1, 5)  # Каждый пользователь делает запрос раз в 1-5 секунд

    @task(3)
    def load_home_page(self):
        """Тестируем главную страницу"""
        self.client.get("/")

    @task(2)
    def load_product_list(self):
        """Тестируем страницу списка товаров"""
        self.client.get("/products/")

    @task(2)
    def load_category_page(self):
        """Тестируем страницу категории"""
        self.client.get("/category/test-category/")

    @task(1)
    def load_product_detail(self):
        """Тестируем страницу товара"""
        self.client.get("/detail/test-product/")

    @task(1)
    def search_products(self):
        """Тестируем поиск"""
        self.client.get("/products/?q=test")

    @task(1)
    def filter_products(self):
        """Тестируем фильтр по цене"""
        self.client.get("/products/?price_min=50&price_max=200")

    @task(1)
    def sort_products(self):
        """Тестируем сортировку"""
        self.client.get("/products/?sort=price_desc")
