from django.shortcuts import render
from .models import Piercing




def index(request):
    piercings = Piercing.objects.all()
    context = {'piercings': piercings}
    return render(request, 'shop/index.html', context=context)


def product_detail(request):
    return render(request, 'shop/product-detail.html')


def product_list(request):
    return render(request, 'shop/products.html')
