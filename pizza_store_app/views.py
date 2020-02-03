from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Category, Product


def catalog(request):
    products = []

    categories = Category.objects.all().order_by('display_order')
    for cat in categories:
        category_products = Product.objects.filter(category=cat).order_by('-price')
        if category_products:
            products.append([cat, category_products])

    context = {
        'products': products
    }
    return render(request, 'pizza_store_app/catalog.html', context)


def product_detail(request, product_id):
    return HttpResponse('Product page ' + str(product_id))


def cart(request):
    return HttpResponse('Cart page')


def make_order(request):
    return HttpResponse('Success page')


def order_history(request):
    return HttpResponse('Orders history')


def order_details(request):
    return HttpResponse('Order details')
