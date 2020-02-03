from django.urls import path
from . import views

app_name = 'pizza_store_app'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('cart', views.cart, name='cart'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('orders', views.order_history, name='order_history'),
    path('orders/<int:order_id>', views.order_details, name='order_details'),
    path('make_order', views.make_order, name='make_order'),
]
