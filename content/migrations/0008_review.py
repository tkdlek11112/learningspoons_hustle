# Generated by Django 3.2.10 on 2022-01-19 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('nickname', models.TextField()),
            ],
        ),
    ]
