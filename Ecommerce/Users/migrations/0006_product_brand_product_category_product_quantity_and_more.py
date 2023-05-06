# Generated by Django 4.2 on 2023-05-01 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default='anything', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='anything', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Users.client'),
        ),
    ]