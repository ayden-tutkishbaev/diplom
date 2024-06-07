# Generated by Django 5.0.4 on 2024-06-06 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_checkout_remove_cartitem_order_and_more'),
        ('profiles', '0004_delete_checkout_remove_order_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.order', verbose_name='Order'),
        ),
    ]