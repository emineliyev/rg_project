# 1. Встроенные библиотеки Python
from datetime import timedelta

# 2. Django и сторонние библиотеки
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.db.models import Q, Max, Min

# 3. Импорты из проекта
from cart.forms import CartAddProductForm
from parameters.models import Contact, Feature
from partners.models import Partner
from shop.forms import CommentForm
from shop.models import Category, Product, SuperSale
from slider.models import Slider


class HomeProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        # Предварительная загрузка связанных данных
        products_query = Product.objects.prefetch_related(
            'images', 'comments'
        ).select_related('category', 'material')

        context.update({
            'products': products_query[:8],
            'new_products': products_query.filter(create_at__gte=now() - timedelta(days=30))[:8],
            'popular_products': products_query.filter(popularity__gt=100)[:8],
            'sliders': Slider.objects.all()[:3],
            'super_sales': SuperSale.objects.select_related('product')[:1],
            'partners': Partner.objects.all(),
            'features': Feature.objects.all(),
        })

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущий товар
        product = self.object

        # Изображения, видео, весовые опции, форма корзины
        context['images'] = product.images.all()
        context['video'] = product.video
        context['weight_options'] = product.weight_options.all()
        context['cart_product_form'] = CartAddProductForm()

        # Комментарии
        context['comment_form'] = CommentForm()
        context['comments'] = product.comments.all()
        context['comments_count'] = product.comments.count()

        # Похожие товары (по категории, исключая текущий товар)
        context['related_products'] = Product.objects.filter(
            category=product.category  # Совпадает категория
        ).exclude(id=product.id)[:6]  # Исключаем текущий товар, берем только 4 товара

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = self.object
            comment.save()
            return HttpResponseRedirect(self.request.path_info)
        context = self.get_context_data(comment_form=comment_form)
        return self.render_to_response(context)


class BaseProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_ordering(self):
        """Возвращает параметр сортировки из GET-запроса."""
        sort_option = self.request.GET.get('sort')
        sort_mapping = {
            "name": "name",
            "price_asc": "price",
            "price_desc": "-price",
            "newest": "-create_at",
        }
        return sort_mapping.get(sort_option)

    def get_queryset(self):
        """Формирует queryset с фильтрацией, поиском и сортировкой."""
        queryset = super().get_queryset().select_related('category', 'material').prefetch_related('images')

        # Фильтрация по цене
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        if price_min:
            try:
                price_min = float(price_min.replace(',', '.'))
                queryset = queryset.filter(price__gte=price_min)
            except ValueError:
                pass  # Игнорируем некорректные значения

        if price_max:
            try:
                price_max = float(price_max.replace(',', '.'))
                queryset = queryset.filter(price__lte=price_max)
            except ValueError:
                pass  # Игнорируем некорректные значения

        # Фильтрация по поисковому запросу
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        # Применяем сортировку
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет в контекст данные для фильтрации, сортировки и поиска."""
        context = super().get_context_data(object_list=object_list, **kwargs)

        # Вычисляем диапазон цен
        price_range = Product.objects.aggregate(max_price=Max('price'), min_price=Min('price'))
        max_price = price_range['max_price']
        min_price = price_range['min_price']

        # Получаем текущие значения фильтров
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        def clean_price(value, default):
            """Преобразует строку в float, заменяя запятую на точку."""
            if value:
                try:
                    return float(value.replace(',', '.'))
                except ValueError:
                    pass
            return default

        context.update({
            'categories': Category.objects.all(),
            'popular_products': Product.objects.filter(popularity__gt=100).prefetch_related('images')[:3],
            'max_salary': max_price,
            'min_salary': min_price,
            'current_price_min': clean_price(price_min, min_price),
            'current_price_max': clean_price(price_max, max_price),
            'current_sort': self.request.GET.get('sort', ''),
            'query': self.request.GET.get('q', ''),
            'product_count': self.get_queryset().count(),
            'all_products': Product.objects.all().count(),
        })
        return context


class ProductListView(BaseProductListView):
    pass


class CategoryProductListView(BaseProductListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            queryset = queryset.filter(category__in=category.get_descendants(include_self=True))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['current_category'] = category
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ContactListView(ListView):
    model = Contact
    template_name = 'shop/contact.html'
    context_object_name = 'contacts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context
