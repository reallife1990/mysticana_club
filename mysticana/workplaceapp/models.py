from django.db import models
from authapp.models import User
from uuid import uuid4
from datetime import datetime


class MainClients(models.Model):
    first_name = models.CharField(max_length=25, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=True, verbose_name='Фамилия')
    city = models.CharField(max_length=20, blank=True, verbose_name="Город")
    photo = models.ImageField(blank=True, upload_to="photo/clients/", verbose_name="Фото")
    born_date = models.DateField(blank=True, verbose_name="Дата рождения")
    born_time = models.TimeField(null=True, blank=True, verbose_name="Время рождения")
    date_created = models.DateTimeField(default=datetime.now, verbose_name="Дата добавления")
    telephone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    viber = models.BooleanField(default=False, verbose_name="Viber")
    whatsup = models.BooleanField(default=False, verbose_name="Whatsup")
    telegram = models.CharField(max_length=50, blank=True, verbose_name="Telegram")
    instagram = models.CharField(max_length=50, blank=True, verbose_name="Instagram")
    vk = models.CharField(max_length=50, blank=True, verbose_name="ВК")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'