import base64
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

class Reduction:
    """
    incoming INT
    """

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
        ф-ция для данных видического расчёта
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


class TablePifagora():
    """

       self: born_date(objectdatetime)
    """
    # def calculate(self, method='std'):
    #     # std стандартное сокращение до однозначного числа
    #     # for_pi для таблицы пифагора , не сокращается
    #     # for_pi_limit для таблицы пифагора , не сокращается 10 11 и 12
    #     day = str(self.day)
    #     month = str(self.month)
    #     year = str(self.year)
    #     str_date=str(self.day)+str(self.month)+str(self.year)
    #
    #
    #     res = 0
    #     for el in str_date:
    #         res += int(el)
    #     if method == 'for_pi':
    #         return res
    #     elif method == 'for_pi_limit' and res in [10, 11, 12]:
    #         return res
    #     else:
    #         while res > 9:
    #             res = res // 10 + res % 10
    #         return res
    def data_table(self):
        """

        :return: словарь квадрата
        """
        CALC_RULES={1:[10,13,17], 2:[11,13], 3:[12,13,16],
                    4:[10,14], 5:[11,14,16,17], 6:[12,14],
                    7:[10,15,16], 8:[11,15], 9:[12,15,17]}
        numbers=TablePifagora.work_numbers(self)[0:4]
        string=TablePifagora.date_to_str(self)
        for i in numbers:
            string+=str(i)
        table_nums = []
        for i in range(1, 10):
            if string.count(str(i)) == 0:
                table_nums.append('-')
            else:
                table_nums.append(str(i) * (string.count(str(i))))
        # print(table_nums)  #['1', '222', '-', '-', '-', '-', '-', '888', '9']
        table_dict = dict.fromkeys(range(1,18),0)

        for k,v  in enumerate(range(1, 10),1):
            volume =string.count(str(v))
            for i in CALC_RULES.get(k):
                table_dict[i]=table_dict.get(i)+volume
            if volume == 0:
                table_dict[k]= '-'
            else:
                table_dict[k]=str(v) * volume
        conv=f'{table_dict.pop(16)}/{table_dict.pop(17)}'
        table_dict[16]=conv
        print(table_dict) #{1: 1, 2: 3, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 3, 9: 1}
        # TablePifagora.special_values(table_dict)
        return table_dict




    def data_answer(self):
        NAMES = ['', 'Характер', 'Энергия', 'Интерес',
                 'Здоровье', 'Логика', 'Труд',
                 'Удача', 'Долг', 'Память',
                 'Цель', 'Семья', 'Привычки',
                 'Самооценка', 'Работа', 'Талант',
                 'Темперамент/Дух']
        RULES =[[1, 4, 7, 10],[2, 5, 8, 11], [3, 6, 9, 12], [13, 14, 15, 16]]
        DATA = TablePifagora.data_table(self)
        WORK_NUMB = TablePifagora.work_numbers(self)
        data_table=[]
        for rule in RULES:
            row=[]
            for elem in rule:
                row.append({'elem':elem, 'name': NAMES[elem],'data':DATA[elem]})
            data_table.append(row)
        print(data_table)
        answ = {"work_numb": WORK_NUMB[:4], "data": data_table, '4gp':WORK_NUMB[4]}
        return answ

    def work_numbers(self):
        """
        рабочие числа:
        1е - сумма всех в дате
        2е - сокращение 1го до однозначного при >12
        3е - модуль(1е - 2* на первое число дня рождения)
        4е -  сокращение 3го до однозначного при >12
        ЧЖП = сокращение 1го при >9
        :return:

        """
        str_date = TablePifagora.date_to_str(self)
        first = Reduction.for_pi(str_date)
        second =Reduction.for_pi_limit(first)

        three =abs(first - 2*int(str(self.day)[0]))
        four = Reduction.for_pi_limit(three)
        num_life_way =Reduction.std(second)
        return [first,second,three,four, num_life_way]

    def date_to_str(self):
        str_date = str(self.day) + str(self.month) + str(self.year)
        return str_date
