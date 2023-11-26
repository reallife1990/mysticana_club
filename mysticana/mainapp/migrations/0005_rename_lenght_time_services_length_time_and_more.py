# Generated by Django 4.1.5 on 2023-05-13 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_services_formats'),
    ]

    operations = [
        migrations.RenameField(
            model_name='services',
            old_name='lenght_time',
            new_name='length_time',
        ),
        migrations.AlterField(
            model_name='services',
            name='formats',
            field=models.ManyToManyField(to='mainapp.formatservice', verbose_name='Формат проведения'),
        ),
    ]