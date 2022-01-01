# Generated by Django 3.2.10 on 2022-01-01 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField()),
                ('seller', models.TextField()),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]
