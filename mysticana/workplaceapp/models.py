import uuid

from django.db import models
from authapp.models import User
from uuid import uuid4
from datetime import datetime, timezone
from .utils import Reduction, Calculate, TablePifagora


class MainClients(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=25, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=True, verbose_name='Фамилия')
    city = models.CharField(max_length=20, blank=True, verbose_name="Город")
    photo = models.ImageField(blank=True, upload_to="photo/clients/", verbose_name="Фото")
    born_date = models.DateField(blank=True, verbose_name="Дата рождения")
    born_time = models.TimeField(null=True, blank=True, verbose_name="Время рождения")
    date_created = models.DateTimeField(default=datetime.now(), verbose_name="Дата добавления")
    telephone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    viber = models.BooleanField(default=False, verbose_name="Viber")
    whatsup = models.BooleanField(default=False, verbose_name="Whatsup")
    telegram = models.CharField(max_length=50, blank=True, verbose_name="Telegram")
    instagram = models.CharField(max_length=50, blank=True, verbose_name="Instagram")
    vk = models.CharField(max_length=50, blank=True, verbose_name="ВК")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")

    # произвольное вычисляемое поле толькодля отбражения и внутренних дел
    #  с базой не взаимодействует
    @property
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
        return f'{years} {txt}'

    @property
    def info(self):
        """
        :return: массив с данными для отображения:
                main_tbl -основной видический расчёт
        """

        d = {}
        d['a'] = Reduction.std(self.born_date.year)
        d['b'] = Reduction.for_pi(self.born_date.year)
        d['c'] = Reduction.for_pi_limit(self.born_date.year)
        d['d'] = {"re":20}
        d['main_tbl'] = Calculate.main_table(self.born_date, self.age)
        d['work_numbers'] = TablePifagora.work_numbers(self.born_date)
        d['work_numbersss'] = TablePifagora.data_table(self.born_date)
        return d
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'