import math

# Программа для решения кубических уравнений по формуле Кардано (в 
# действительных числах). 
# Напишите программу, которая принимает от пользователя действительные 
# коэффициенты a, b, c, d для уравнения: 
# ax^3 + bx^2 + cx + d = 0 (при a ≠ 0) 
# Программа должна переводить уравнение к каноническому виду: 
# y^3 + py + q = 0 
# где коэффициенты вычисляются по формулам: 
# p = (3ac - b^2) / (3a^2) 
# q = (2b^3 - 9abc + 27a^2 * d) / (27a^3) 
# Далее необходимо рассчитать кубический дискриминант: 
# D = (q/2)^2 + (p/3)^3 
# Анализируя знак дискриминанта с помощью условного оператора, программа 
# должна вывести текстовое сообщение о том, сколько именно действительных 
# корней имеет уравнение (1, 2 или 3), а затем вычислить и напечатать сами 
# действительные корни, выполнив обратную подстановку: 
# x = y - b/(3a) 
# При извлечении кубических корней из отрицательных чисел обеспечьте 
# корректную работу алгоритма без выхода в комплексную плоскость (используя 
# свойства знака числа или функцию math.copysign).

class Equation:
    def __init__(self, a: float, b: float, c: float, d: float):
        if a == 0:
            print("Коэффициент 'a' не должен быть равен 0 для кубического уравнения.")
            return
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def _cbrt(val: float) -> float:
        return math.copysign(abs(val) ** (1 / 3), val)

    def canonical_form(self):
        p = (3 * self.a * self.c - self.b ** 2) / (3 * self.a ** 2)
        q = (2 * self.b ** 3 - 9 * self.a * self.b * self.c + 27 * self.a ** 2 * self.d) / (27 * self.a ** 3)
        return p, q

    def calculate_discriminant(self, p: float, q: float) -> float:
        return (q / 2) ** 2 + (p / 3) ** 3

    def reverse_substitution(self, y: float) -> float:
        return y - self.b / (3 * self.a)

    def solve(self):
        p, q = self.canonical_form()
        disc = self.calculate_discriminant(p, q)

        if abs(disc) < 1e-12:
            disc = 0.0

        if disc > 0:
            print("Уравнение имеет 1 действительный корень.")
            u = self._cbrt(-q / 2 + disc ** 0.5)
            v = self._cbrt(-q / 2 - disc ** 0.5)
            y1 = u + v
            return [self.reverse_substitution(y1)]

        elif disc == 0:
            if p == 0 and q == 0:
                print("Уравнение имеет 1 действительный корень кратного типа.")
                return [self.reverse_substitution(0.0)]

            print("Уравнение имеет 2 действительных корня.")
            u = self._cbrt(-q / 2)
            y1 = 2 * u
            y2 = -u
            return [self.reverse_substitution(y1), self.reverse_substitution(y2)]

        else:
            print("Уравнение имеет 3 действительных корня.")
            r = (-p / 3) ** 0.5
            cos_arg = max(-1.0, min(1.0, -q / (2 * r ** 3)))
            theta = math.acos(cos_arg)
            
            y1 = 2 * r * math.cos(theta / 3)
            y2 = 2 * r * math.cos((theta + 2 * math.pi) / 3)
            y3 = 2 * r * math.cos((theta + 4 * math.pi) / 3)
            
            return [
                self.reverse_substitution(y1),
                self.reverse_substitution(y2),
                self.reverse_substitution(y3)
            ]

if __name__ == '__main__':
    eq = Equation(-1, 0, -3, 2)
    roots = eq.solve()

    print("Корни уравнения:")
    for idx, root in enumerate(roots, 1):
        print(f"x{idx} = {root}")
