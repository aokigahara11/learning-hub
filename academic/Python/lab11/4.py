import cmath

# Программа для решения уравнений 4-й степени по методу Феррари в 
# комплексных числах. 
# Реализуйте универсальный метод Феррари для поиска всех корней уравнения 4-й 
# степени на комплексной плоскости. Программа должна использовать комплексный 
# модуль cmath на каждом этапе: от нахождения корня резольвенты до решения 
# результирующих квадратных уравнений. Пользователь вводит коэффициенты, а 
# программа рассчитывает и выводит на экран все 4 корня исходного уравнения, 
# независимо от того, являются они вещественными или комплексными.

class Equation:
    def __init__(self, a: complex, b: complex, c: complex, d: complex, e: complex):
        if a == 0:
            print("Коэффициент 'a' не должен быть равен 0 для уравнения 4-й степени.")
            return
        self.a = complex(a)
        self.b = complex(b)
        self.c = complex(c)
        self.d = complex(d)
        self.e = complex(e)

    def canonical_form(self):
        """Сводит ax^4 + bx^3 + cx^2 + dx + e = 0 к y^4 + py^2 + qy + r = 0."""
        a, b, c, d, e = self.a, self.b, self.c, self.d, self.e
        p = (8 * a * c - 3 * b**2) / (8 * a**2)
        q = (b**3 - 4 * a * b * c + 8 * a**2 * d) / (8 * a**3)
        r = (-3 * b**4 + 256 * a**3 * e - 64 * a**2 * b * d + 16 * a * b**2 * c) / (256 * a**4)
        return p, q, r

    def ferari_resolvent(self, p: complex, q: complex, r: complex):
        """Формирует коэффициенты кубической резольвенты: t^3 - p*t^2 - 4r*t + (4pr - q^2) = 0."""
        return 1.0 + 0j, -p, -4.0 * r, 4.0 * p * r - q**2

    def _solve_cubic_complex(self, A: complex, B: complex, C: complex, D: complex) -> complex:
        """Находит один комплексный корень кубической резольвенты методом Кардано в cmath."""
        b_c, c_c, d_c = B / A, C / A, D / A

        # Приведенный вид z^3 + p_c*z + q_c = 0 (где t = z - b_c/3)
        p_c = c_c - (b_c**2) / 3.0
        q_c = (2.0 * b_c**3) / 27.0 - (b_c * c_c) / 3.0 + d_c

        discriminant = (p_c / 3.0)**3 + (q_c / 2.0)**2

        # Извлечение квадратного корня через cmath
        sqrt_discriminant = cmath.sqrt(discriminant)

        # Вычисление u (кубический корень в комплексной области)
        u = (-q_c / 2.0 + sqrt_discriminant) ** (1.0 / 3.0)

        # Вычисление v: если u == 0, берем корень из второй ветви
        if u == 0:
            v = (-q_c / 2.0 - sqrt_discriminant) ** (1.0 / 3.0)
        else:
            v = -p_c / (3.0 * u)

        z = u + v
        return z - b_c / 3.0

    def solve(self):
        p, q, r = self.canonical_form()

        # Случай, когда q == 0 (биквадратное уравнение)
        if abs(q) < 1e-12:
            disc_y = p**2 - 4.0 * r
            sqrt_disc = cmath.sqrt(disc_y)
            y2_1 = (-p + sqrt_disc) / 2.0
            y2_2 = (-p - sqrt_disc) / 2.0

            y1 = cmath.sqrt(y2_1)
            y2 = -y1
            y3 = cmath.sqrt(y2_2)
            y4 = -y3

            shift = self.b / (4.0 * self.a)
            return [y1 - shift, y2 - shift, y3 - shift, y4 - shift]

        # Формируем кубическую резольвенту
        A, B, C, D = self.ferari_resolvent(p, q, r)

        # Находим корень резольвенты t
        t = self._solve_cubic_complex(A, B, C, D)

        # Извлекаем квадратный корень sqrt(2t - p)
        sqrt_2t_p = cmath.sqrt(2.0 * t - p)

        # Разложение на два квадратных уравнения:
        # y^2 + sqrt(2t - p)*y + (t - q / (2 * sqrt(2t - p))) = 0
        # y^2 - sqrt(2t - p)*y + (t + q / (2 * sqrt(2t - p))) = 0
        k = q / (2.0 * sqrt_2t_p)

        b1, c1 = sqrt_2t_p, t - k
        b2, c2 = -sqrt_2t_p, t + k

        # Решение первого квадратного уравнения относительно y
        d1 = b1**2 - 4.0 * c1
        sqrt_d1 = cmath.sqrt(d1)
        y1 = (-b1 + sqrt_d1) / 2.0
        y2 = (-b1 - sqrt_d1) / 2.0

        # Решение второго квадратного уравнения относительно y
        d2 = b2**2 - 4.0 * c2
        sqrt_d2 = cmath.sqrt(d2)
        y3 = (-b2 + sqrt_d2) / 2.0
        y4 = (-b2 - sqrt_d2) / 2.0

        # Переход обратно к x = y - b / (4a)
        shift = self.b / (4.0 * self.a)
        return [y1 - shift, y2 - shift, y3 - shift, y4 - shift]

    def print_roots(self):
        roots = self.solve()
        print("Все 4 корня уравнения:")
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
        eq = Equation(1, -10, 35, -50, 24) # (корни: 1, 2, 3, 4)
        eq.print_roots()