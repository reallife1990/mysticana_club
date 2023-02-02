
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
