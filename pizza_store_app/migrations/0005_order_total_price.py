# Generated by Django 3.0.2 on 2020-02-06 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_store_app', '0004_auto_20200206_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0, verbose_name='Итоговая цена в евро'),
            preserve_default=False,
        ),
    ]
