# Generated by Django 5.0.4 on 2024-06-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_checkout_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='total_price',
            field=models.FloatField(default=0, verbose_name='Total price'),
        ),
    ]
