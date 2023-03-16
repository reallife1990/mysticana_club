import base64
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

import numpy as np


class Reduction:
    # def __init__(self):
    #     value = self.value

    def reduction(self):
        # суммирование цифр
        res = 0
        for el in str(self):
            res += int(el)
            # print(res)
        return res

    def std(self):
        # std стандартное сокращение до однозначного числа
        res = Reduction.reduction(self)
        while res > 9:
            res = res // 10 + res % 10
        return res

    def for_pi(self):
        # for_pi для таблицы пифагора , не сокращается
        return Reduction.reduction(self)

    def for_pi_limit(self):
        # for_pi_limit для таблицы пифагора , не сокращается 10 11 и 12
        if Reduction.reduction(self) in [10, 11, 12]:
            return Reduction.reduction(self)
        else:
            return Reduction.std(self)


class Calculate:
    # def __init__(self, date_user):
    #      date_us = self.date_user

    def main_table(self, age):
        """

        :param age: возраст
        :return: dict: 'num_char'- число характера
                'way'- подход
                'method' - метод
                'expr' - экспрессия
                'karm'- карма
                'trable' - проблема воплощения
                'sol_year' -  солярный год
        """
        result = {}
        result['num_char'] = Reduction.std(self.day)  # чх
        result['way'] = Reduction.std(self.month)  # подход
        result['method'] = Reduction.std(self.year)  # метод
        result['expr'] = Reduction.std(result.get('num_char')+result.get('way'))  # экспрессия
        result['karm'] = Reduction.std(result.get('method')+result.get('expr'))  # карма
        result['trable'] = Reduction.std(abs(
            (result.get('num_char') - result.get('way')) -
            (result.get('num_char') - result.get('method'))
             ))  # проблема воплощения

        if datetime.now().year - self.year == age:
            # солярный год
            result['sol_year'] = Reduction.std(result.get("expr") +
                                               Reduction.std(datetime.now().year))
        else:
            result['sol_year'] = Reduction.std(result.get("expr") +
                                               Reduction.std((datetime.now().year)-1))

        return result

class DrawGraph:

    def calculate_data(self):
        """
        self: born_date(object datetime)
        словарь для отрисовки графика
        :return: dict: sy(list) - судьба !!!значения int!!!
                       vol(list) - воля
        """
        year = self.year
        other = self.day*100+self.month
        sy = list(str(year*other))
        vol = list(str(int(str(year).replace('0','1'))*int(str(other).replace('0','1'))))
        if len(sy) < 7:
            sy.insert(0,'0')
        if len(vol) < 7:
            vol.insert(0,'0')
        result = {'sy': [], 'vol': [],}
        for i in sy:
            result['sy'].append(int(i))
        for i in vol:
            result['vol'].append(int(i))
        print(result)
        return result

    @staticmethod
    def get_graph():
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph
    @staticmethod
    def get_plot(data, age):
        d= DrawGraph.calculate_data(data)

        vol = d.get('vol')
        sy = d.get('sy')
        now = int(age.split(' ')[0])
        print(vol, sy, now)
        x = [0, 12, 24, 36, 48, 60, 72]
        plt.switch_backend('AGG') # запись в файл
        fig, ax = plt.subplots()
        plt.title('График судьбы и воли', fontsize=14)
        plt.grid()
        line = ax.plot(x, vol, c='r')
        line2 = ax.plot(x, sy, c='g')
        line3 = ax.vlines(now, 0, 9)  # сейчас
        plt.setp(line, linestyle='--', c='g', label='график воли')
        plt.setp(line2, linestyle='-', c='r', label='график судьбы')
        plt.setp(line3, color='b')
        plt.xlabel('возраст', fontsize=14)
        plt.ylabel('сила действия', fontsize=14)
        plt.xticks(range(0, 73, 12), fontsize=14)
        plt.yticks(range(0, 10, 1), fontsize=14)

        plt.tight_layout()
        fig.set_figwidth(11)
        fig.set_figheight(7)

        plt.legend(fontsize=12, shadow=True, framealpha=1, facecolor='yellow',
                   edgecolor='r', title='Легенда', loc='best')

        graph = DrawGraph.get_graph()
        return graph

