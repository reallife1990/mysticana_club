from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from datetime import datetime
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, verbose_name="id")
    email = models.EmailField(unique=True, verbose_name='Email')
    confirm_email = models.BooleanField(default=False, verbose_name="Подтвержение")
    is_client = models.BooleanField(default=False, verbose_name="Клиент")
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


