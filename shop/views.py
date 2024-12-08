from django.shortcuts import render

def index(request):
    return render(request, 'shop/index.html')


def product_detail(request):
    return render(request, 'shop/product-detail.html')

def product_list(request):
    return render(request, 'shop/products.html')