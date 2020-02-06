from django.contrib import admin
from .models import Product, Customer, CartItem, Order, OrderedItem, SellingParameter, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(SellingParameter)
