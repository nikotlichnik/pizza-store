# Generated by Django 3.0.2 on 2020-02-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_store_app', '0005_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(verbose_name='Итоговая цена в евро'),
        ),
    ]
