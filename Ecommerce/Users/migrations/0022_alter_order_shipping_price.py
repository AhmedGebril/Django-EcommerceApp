# Generated by Django 4.2 on 2023-05-03 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0021_alter_order_tax_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_price',
            field=models.IntegerField(default=30),
        ),
    ]
