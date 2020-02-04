from django.apps import AppConfig


class PizzaStoreAppConfig(AppConfig):
    name = 'pizza_store_app'
    verbose_name = 'Заказ пиццы'

    def ready(self):
        import pizza_store_app.signals
