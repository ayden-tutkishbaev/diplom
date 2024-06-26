# Generated by Django 5.0.4 on 2024-06-06 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_orderproduct_order_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.order', verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order_products', to='profiles.orderproduct', verbose_name='items'),
        ),
    ]
