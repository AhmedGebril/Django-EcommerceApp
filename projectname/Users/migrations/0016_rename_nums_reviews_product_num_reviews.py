# Generated by Django 4.2 on 2023-05-03 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0015_rename_nums_rating_product_nums_reviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='nums_reviews',
            new_name='num_reviews',
        ),
    ]