# Generated by Django 4.2 on 2023-05-03 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0012_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
