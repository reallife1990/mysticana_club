from django.db import models

# Create your models here.
from mysticana import settings

NULLABLE = {'blank': True, 'null': True}


class BasicData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    # создание абстрактного класса, все поля этого класса добавятся в модели-дочери при
    # наследовании

    class Meta:
        abstract = True


class News(BasicData):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=256, verbose_name='Вступление')

    body = models.TextField(verbose_name='Содержание')
    body_as_markdown = models.BooleanField(default=False, verbose_name="Разметка")
    image = models.ImageField(blank=True, upload_to="images/news/", verbose_name="Картинка")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Services(BasicData):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=256, verbose_name='Вступление')

    body = models.TextField(verbose_name='Описание')
    body_as_markdown = models.BooleanField(default=False, verbose_name="Разметка")
    image = models.ImageField(blank=True, upload_to="photo/services/", verbose_name = "Картинка")

    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Стоимость', default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'