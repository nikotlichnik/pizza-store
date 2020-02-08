from django.shortcuts import render, redirect, reverse, get_object_or_404, Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Product, CartItem, Customer, SellingParameter, OrderedItem, Order
from .forms import CustomerForm

MIN_PIZZA_COUNTER = 1
DOLLAR_TO_EURO_RATE = 0.91
DELIVERY_PRICE_KEY = 'DELIVERY_PRICE'


def catalog(request):
    products = []
    categories = Category.objects.all().order_by('display_order')
    for cat in categories:
        category_products = Product.objects.filter(category=cat).order_by('-price')
        if category_products:
            products.append([cat, category_products])

    context = {
        'products': products,
        'cart_info': get_user_cart_info(request.user)
    }
    return render(request, 'pizza_store_app/catalog.html', context)


@login_required()
def add_to_cart(request):
    anchor = ''

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

        anchor = '#' + str(product.id)

    return redirect(reverse('pizza_store_app:catalog') + anchor)


@login_required()
def change_cart_quantity(request):
    anchor = ''

    if request.method == 'POST':
        print(request.POST['action'])
        action = request.POST['action']
        product_id = request.POST['product_id']
        product = get_object_or_404(Product, pk=product_id)
        cart_item = get_object_or_404(CartItem, customer=request.user.customer, product=product)
        if action == 'minus':
            cart_item.quantity -= 1
        elif action == 'plus':
            cart_item.quantity += 1

        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        anchor = '#' + str(product_id)

    return redirect(reverse('pizza_store_app:cart') + anchor)


def get_usd_price(eur_price):
    return round(eur_price / DOLLAR_TO_EURO_RATE, 2)


def get_user_cart_info(user_obj):
    """
    :param user_obj: User object
    :return: cart items counter and cart total price (eur and usd)
    """
    items_counter = 0
    cart_price_eur = 0
    cart_price_usd = 0
    total_price_eur = 0
    total_price_usd = 0

    delivery_price_eur = SellingParameter.objects.get(key=DELIVERY_PRICE_KEY).value
    delivery_price_usd = get_usd_price(delivery_price_eur)

    if user_obj.is_authenticated:
        cart_items = user_obj.customer.cartitem_set.all()
        for item in cart_items:
            items_counter += item.quantity
            cart_price_eur += round(item.quantity * item.product.price, 2)

    cart_price_usd = get_usd_price(cart_price_eur)

    total_price_eur = round(cart_price_eur + delivery_price_eur, 2)
    total_price_usd = round(cart_price_usd + delivery_price_usd, 2)

    return {'counter': items_counter,
            'cart_total_eur': cart_price_eur,
            'cart_total_usd': cart_price_usd,
            'delivery_price_eur': delivery_price_eur,
            'delivery_price_usd': delivery_price_usd,
            'total_price_eur': total_price_eur,
            'total_price_usd': total_price_usd,
            }


@login_required()
def cart(request):
    cart_items = []
    customer = Customer.objects.get(user=request.user)

    cart_items_set = CartItem.objects.filter(customer=customer).order_by('pk')
    for item in cart_items_set:
        cart_items.append({
            'id': item.product.id,
            'name': item.product.name,
            'image': item.product.image,
            'quantity': item.quantity,
            'price': item.quantity * item.product.price
        })

    context = {
        'cart_items': cart_items,
        'cart_info': get_user_cart_info(request.user)
    }

    return render(request, 'pizza_store_app/cart.html', context)


def transfer_cart_to_order(customer, order_obj):
    for cart_item in customer.cartitem_set.all():
        product = cart_item.product
        quantity = cart_item.quantity
        price = cart_item.product.price

        OrderedItem.objects.create(order=order_obj, product=product, quantity=quantity, price_per_item=price)
        cart_item.delete()


@login_required()
def checkout(request):
    customer = request.user.customer
    customer_form = CustomerForm(instance=customer)
    cart_info = get_user_cart_info(request.user)

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)
        customer_form.save()

        comment = request.POST['order_comment']
        phone = customer.phone
        address = customer.address
        total_price = cart_info['total_price_eur']

        order_obj = Order.objects.create(customer=customer, contact_phone=phone, address=address, comment=comment,
                                         total_price=total_price)

        transfer_cart_to_order(customer, order_obj)

        return redirect(reverse('pizza_store_app:order_details', args=(order_obj.id,)))

    context = {
        'cart_info': get_user_cart_info(request.user),
        'form': customer_form,
    }

    return render(request, 'pizza_store_app/order.html', context)


@login_required()
def order_history(request):
    order_list = Order.objects.filter(customer=request.user.customer)

    context = {
        'cart_info': get_user_cart_info(request.user),
        'order_list': order_list,
    }

    return render(request, 'pizza_store_app/order_history.html', context)


@login_required()
def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user.customer)

    context = {
        'cart_info': get_user_cart_info(request.user),
        'order': order,
    }

    return render(request, 'pizza_store_app/order_detail.html', context)
