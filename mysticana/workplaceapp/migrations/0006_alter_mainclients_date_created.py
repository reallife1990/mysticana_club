# Generated by Django 4.1.5 on 2023-05-12 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workplaceapp', '0005_delete_services_alter_mainclients_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainclients',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 9, 55, 12, 313046), verbose_name='Дата добавления'),
        ),
    ]