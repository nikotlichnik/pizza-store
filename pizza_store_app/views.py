from django.shortcuts import render, redirect, reverse, get_object_or_404, Http404
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Category, Product, CartItem, Customer

MIN_PIZZA_COUNTER = 1
MAX_PIZZA_COUNTER = 100


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


@login_required()
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product_quantity = int(request.POST['product_quantity'])

        if product_quantity < MIN_PIZZA_COUNTER:
            return Http404

        product = get_object_or_404(Product, pk=product_id)
        customer = Customer.objects.get(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(customer=customer, product=product,
                                                            defaults={'quantity': product_quantity})
        if not created:
            cart_item.quantity += product_quantity
            cart_item.save()

    return redirect(reverse('pizza_store_app:catalog'))


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
