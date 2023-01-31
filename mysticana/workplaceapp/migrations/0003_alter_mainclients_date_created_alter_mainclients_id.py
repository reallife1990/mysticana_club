# Generated by Django 4.1.5 on 2023-01-31 20:36

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('workplaceapp', '0002_alter_mainclients_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainclients',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 31, 23, 36, 22, 424647), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='mainclients',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]