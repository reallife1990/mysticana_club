# Generated by Django 4.1.5 on 2023-01-29 18:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workplaceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainclients',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 29, 21, 55, 20, 653530), verbose_name='Дата добавления'),
        ),
    ]