import uuid
from django.contrib import admin
from django.db import models
from authapp.models import User
from uuid import uuid4
from datetime import datetime, timezone
from .utils import Reduction, Calculate, TablePifagora
from mainapp.models import Services

class MainClients(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=25, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=True, verbose_name='Фамилия')
    city = models.CharField(max_length=20, blank=True, verbose_name="Город")
    photo = models.ImageField(blank=True, upload_to="photo/clients/", verbose_name="Фото")
    born_date = models.DateField(blank=False, verbose_name="Дата рождения")
    born_time = models.TimeField(null=True, blank=True, verbose_name="Время рождения")
    date_created = models.DateTimeField(default=datetime.now(), verbose_name="Дата добавления")
    telephone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    viber = models.BooleanField(default=False, verbose_name="Viber")
    whatsup = models.BooleanField(default=False, verbose_name="Whatsup")
    telegram = models.CharField(max_length=50, blank=True, verbose_name="Telegram")
    instagram = models.CharField(max_length=50, blank=True, verbose_name="Instagram")
    vk = models.CharField(max_length=50, blank=True, verbose_name="ВК")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь", related_name='client')

    # произвольное вычисляемое поле толькодля отбражения и внутренних дел
    #  с базой не взаимодействует
    @property
    @admin.display(description='Возраст')
    def age(self):
        """

        :return: возраст клиента
        """
        years = datetime.now().year - self.born_date.year
        if datetime.now().month < self.born_date.month or \
                (datetime.now().month == self.born_date.month and
                 datetime.now().day < self.born_date.day):
            years -= 1
        txt = ''
        if (years % 10 == 1 and years != 11):
            txt = 'год'
        elif(years % 10 in [2,3,4]):
            txt = 'года'
        else:
            txt = 'лет'
        # print(years)
        return f'{years} {txt}'


    @property
    def info(self):
        """
        :return: массив с данными для отображения:
                main_tbl -основной видический расчёт
        """

        d = {}
        d['main_tbl'] = Calculate.main_table(self.born_date, self.age)
        d['work_numbers'] = TablePifagora.work_numbers(self.born_date)
        d['pifagor'] = TablePifagora.data_answer(self.born_date)
        return d

    # поле для админки
    @admin.display(description='Клиент')
    def admin_name(self):
        return f'{self.first_name} {self.last_name}'


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ServiceClients(models.Model):
    ''' оказанные услуги
     поле related_name  для создания обратной связи между моделями'''
    id = models.UUIDField(primary_key=True, default=uuid4)
    client = models.ForeignKey(MainClients, on_delete=models.CASCADE, verbose_name='Клиент', null=True, related_name='client_of')
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Услуга', null=True, related_name='service_of')
    date = models.DateField(default=datetime.now(), verbose_name='Дата')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    price = models.IntegerField(blank=True, verbose_name='Цена', null=True)

    # @admin.display(description="Client_name")
    # def client_name(self):
    #     return f'{self.client.first_name} {self.client.last_name}'

    class Meta:
        verbose_name= 'Оказанная услуга'
        verbose_name_plural = 'Оказанные услуги'



