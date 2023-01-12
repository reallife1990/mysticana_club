from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    confirm_email = models.BooleanField(default=False, verbose_name="Подтвержение")
    photo = models.ImageField(blank=True, upload_to='users', verbose_name='фото')
    id_client = models.UUIDField(blank=True, null=True)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
