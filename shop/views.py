from django.db.models import Max
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from datetime import timedelta
from django.views.generic import ListView, DetailView, CreateView
from cart.forms import CartAddProductForm
from shop.forms import CommentForm
from shop.models import Product, Category, Comment


class HomeProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = Product.objects.all()[:8]
        context['new_products'] = Product.objects.filter(create_at__gte=now() - timedelta(days=30))[:8]
        context['popular_products'] = Product.objects.filter(popularity__gt=100)[:8]
        return context


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'shop/product-detail.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context['images'] = self.object.images.all()
#         context['weight_options'] = self.object.weight_options.all()
#         context['cart_product_form'] = CartAddProductForm()
#         return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()  # Передача изображений
        context['video'] = self.object.video  # Передача одного видео, если оно есть
        context['weight_options'] = self.object.weight_options.all()
        context['cart_product_form'] = CartAddProductForm()
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['comments_count'] = self.object.comments.count()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = self.object  # Привязка к продукту
            comment.save()
            return HttpResponseRedirect(self.request.path_info)
        context = self.get_context_data(comment_form=comment_form)
        return self.render_to_response(context)


class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['popular_products'] = Product.objects.filter(popularity__gt=100)[:3]
        max_price = Product.objects.aggregate(max=Max('price'))['max']
        context['max_salary'] = max_price
        return context
