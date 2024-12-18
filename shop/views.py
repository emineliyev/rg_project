from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm
from shop.models import Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = Product.objects.all()[:8]
        context['new_products'] = Product.objects.filter(create_at__gte=now() - timedelta(days=30))[:8]
        context['popular_products'] = Product.objects.filter(popularity__gt=100)[:8]
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'shop/product-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['images'] = self.object.images.all()
        context['weight_options'] = self.object.weight_options.all()
        context['cart_product_form'] = CartAddProductForm()
        return context
