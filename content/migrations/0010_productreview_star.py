# Generated by Django 3.2.10 on 2022-01-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='star',
            field=models.IntegerField(default=0),
        ),
    ]
