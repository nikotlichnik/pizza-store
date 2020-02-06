from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    Adds extra fields to User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=1024)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'


class Category(models.Model):
    """
    Describes product categories
    """
    name = models.CharField(verbose_name='Название', max_length=128)
    display_order = models.PositiveSmallIntegerField(verbose_name='Порядок отображения',
                                                     help_text='Чем меньше значение, тем выше в списке')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """
    Describes products in catalog
    """
    name = models.CharField(verbose_name='Название', max_length=256)
    description = models.TextField(verbose_name='Описание', max_length=512)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория продукта', null=True,
                                 blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='img/')
    price = models.PositiveIntegerField(verbose_name='Цена в евро')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class CartItem(models.Model):
    """
    Describes user products at their carts
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return ' -- '.join(map(str, ([self.customer, self.product, self.quantity])))

    class Meta:
        verbose_name = 'продукт корзины'
        verbose_name_plural = 'продукты корзины'


class Order(models.Model):
    """
    Describes customer's order
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    address = models.TextField(verbose_name='Адрес доставки', max_length='1024')
    contact_phone = models.CharField(verbose_name='Контактный номер телефона', max_length=20)
    comment = models.TextField(verbose_name='Комментарий', max_length='1024')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderedItem(models.Model):
    """
    Describes ordered products
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price_per_item = models.PositiveIntegerField(verbose_name='Цена за шт.')

    class Meta:
        verbose_name = 'заказанный продукт'
        verbose_name_plural = 'заказанные продукты'


class SellingParameter(models.Model):
    """
    Describes additional price values
    """
    key = models.CharField(verbose_name='Параметр', max_length=256)
    value = models.PositiveIntegerField(verbose_name='Значение')

    def __str__(self):
        return self.key + ' -- ' + str(self.value)

    class Meta:
        verbose_name = 'параметр'
        verbose_name_plural = 'параметры'
