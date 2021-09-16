# Generated by Django 2.2.19 on 2021-09-14 21:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210914_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество ингредиента: 1 единица')], verbose_name='Количество ингредиента'),
        ),
    ]
