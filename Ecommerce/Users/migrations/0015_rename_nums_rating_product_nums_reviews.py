# Generated by Django 4.2 on 2023-05-03 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0014_product_avg_rating_product_nums_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='nums_rating',
            new_name='nums_reviews',
        ),
    ]