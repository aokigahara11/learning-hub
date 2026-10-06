import cmath
import math

# Программа для решения кубических уравнений по формуле Кардано в 
# комплексных числах. 
# Модифицируйте алгоритм Кардано, используя возможности библиотеки cmath. 
# Программа принимает вещественные или комплексные коэффициенты уравнения. 
# Все вычисления (включая извлечение квадратных и кубических корней) должны 
# выполняться в комплексной форме через функции cmath.sqrt() и оператор 
# возведения в степень комплексного числа. Программа должна находить и 
# выводить на экран абсолютно все 3 корня уравнения (включая сопряженные 
# комплексные пары, если они есть) в формате x = a + bi. При расчете кубического 
# корня из комплексного числа учитывайте, что оператор ** (1/3) возвращает только 
# одно из трех значений; найдите остальные два с помощью формулы: 
# wk = w0 * e^(i * 2 * pi * k / 3) 
# где k принимает значения 1 и 2.

class Equation:
    def __init__(self, a: complex, b: complex, c: complex, d: complex):
        if a == 0:
            print("Коэффициент 'a' не должен быть равен 0 для кубического уравнения.")
            return
        self.a = complex(a)
        self.b = complex(b)
        self.c = complex(c)
        self.d = complex(d)

    def solve(self):
        a, b, c, d = self.a, self.b, self.c, self.d

        # Приведение к каноническому виду y^3 + p*y + q = 0 (замена x = y - b / (3*a))
        p = (3 * a * c - b**2) / (3 * a**2)
        q = (2 * b**3 - 9 * a * b * c + 27 * a**2 * d) / (27 * a**3)

        discriminant = (p / 3)**3 + (q / 2)**2

        sqrt_discriminant = cmath.sqrt(discriminant)

        # Нахождение первого значения кубического корня u0 из (-q/2 + sqrt_discriminant)
        u0 = (-q / 2 + sqrt_discriminant) ** (1 / 3)

        # Вычисление трех значений u с помощью формулы wk = w0 * e^(i * 2 * pi * k / 3)
        e1 = cmath.exp(1j * 2 * math.pi / 3)
        e2 = cmath.exp(1j * 4 * math.pi / 3)

        u_values = [u0, u0 * e1, u0 * e2]

        roots = []
        for u in u_values:
            # Если u == 0, то v = 0, иначе v = -p / (3 * u)
            v = -p / (3 * u) if u != 0 else (-q)**(1/3)
            
            # Корни канонического уравнения y = u + v
            y = u + v
            
            # Переход к исходному неизвестному x = y - b / (3 * a)
            x = y - b / (3 * a)
            roots.append(x)

        return roots

    def print_roots(self):
        roots = self.solve()
        if roots is None:
            return

        for i, root in enumerate(roots, 1):
            real = round(root.real, 6)
            imag = round(root.imag, 6)

            if abs(real) == 0:
                real = 0.0
            if abs(imag) == 0:
                imag = 0.0

            sign = "+" if imag >= 0 else "-"
            print(f"x{i} = {real} {sign} {abs(imag)}i")


if __name__ == "__main__":
    eq = Equation(1, -6, 11, -6) # (корни: 1, 2, 3)
    eq.print_roots()