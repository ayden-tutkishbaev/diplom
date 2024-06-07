# Generated by Django 5.0.4 on 2024-06-03 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(blank=True, choices=[('sent', 'Sent'), ('answered', 'Answered')], default='sent', max_length=50, verbose_name='Status of a message'),
        ),
    ]
