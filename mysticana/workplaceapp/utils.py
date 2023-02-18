from datetime import datetime

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

            result['sol_year'] = Reduction.std(result.get("expr") +
                                               Reduction.std(datetime.now().year))
        else:
            result['sol_year'] = Reduction.std(result.get("expr") +
                                               Reduction.std((datetime.now().year)-1))
            # солярный год
        return result


