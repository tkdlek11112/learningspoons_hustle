# Generated by Django 3.2.10 on 2022-01-23 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_favoriteproducts'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoriteproducts',
            unique_together={('email', 'product_id')},
        ),
    ]
