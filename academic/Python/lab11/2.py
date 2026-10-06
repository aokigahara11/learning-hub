import math

# Программа для решения уравнений 4-й степени по методу Феррари (в 
# действительных числах). 
# Напишите программу, которая принимает от пользователя коэффициенты a, b, c, 
# d, e для уравнения: 
# ax^4 + bx^3 + cx^2 + dx + e = 0 (при a ≠ 0) 
# Программа должна сводить его к приведенному виду: 
# y^4 + p * y^2 + q * y + r = 0 
# и формировать кубическую резольвенту Феррари: 
# t^3 - p * t^2 - 4r * t + (4pr - q^2) = 0 
# Используя вещественный алгоритм Кардано из предыдущей задачи, найдите один 
# действительный корень резольвенты t. С его помощью разложите уравнение на 
# два квадратных уравнения вида: 
# y^2 ± sqrt(2t - p) * y + (t ∓ q / (2 * sqrt(2t - p))) = 0 
# Определите дискриминанты полученных уравнений. Программа должна вывести 
# сообщение о точном количестве действительных корней исходного уравнения (от 
# 0 до 4) и вычислить только те корни, которые являются действительными, 
# выполнив обратную подстановку для перехода от y к x.

class Equation:
    def __init__(self, a: float, b: float, c: float, d: float, e: float):
        if a == 0:
            print("Коэффициент 'a' не должен быть равен 0 для уравнения 4-й степени.")
            return
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.e = float(e)

    def canonical_form(self):
        """Сводит выражение к y^4 + py^2 + qy + r = 0 (замена x = y - b/(4a))."""
        a, b, c, d, e = self.a, self.b, self.c, self.d, self.e
        p = (8 * a * c - 3 * b**2) / (8 * a**2)
        q = (b**3 - 4 * a * b * c + 8 * a**2 * d) / (8 * a**3)
        r = (-3 * b**4 + 256 * a**3 * e- 64 * a**2 * b * d + 16 * a * b**2 * c) / (256 * a**4)
        return p, q, r

    def ferari_resolvent(self, p: float, q: float, r: float):
        """Формирует коэффициенты кубической резольвенты"""
        return 1.0, -p, -4.0 * r, 4.0 * p * r - q**2

    def _solve_cubic_real(self, A: float, B: float, C: float, D: float) -> float:
        # Приведение t^3 + b_c*t^2 + c_c*t + d_c = 0
        b_c, c_c, d_c = B / A, C / A, D / A

        # Приведенный вид z^3 + p_c*z + q_c = 0 (t = z - b_c/3)
        p_c = c_c - (b_c**2) / 3.0
        q_c = (2 * b_c**3) / 27.0 - (b_c * c_c) / 3.0 + d_c

        discriminant = (p_c / 3.0) ** 3 + (q_c / 2.0) ** 2

        if discriminant >= 0:
            sqrt_discriminant = math.sqrt(discriminant)
            u_val = -q_c / 2.0 + sqrt_discriminant
            v_val = -q_c / 2.0 - sqrt_discriminant

            u = math.copysign(abs(u_val) ** (1 / 3), u_val)
            v = math.copysign(abs(v_val) ** (1 / 3), v_val)

            z = u + v
        else:
            r = math.sqrt(-(p_c**3) / 27.0)
            phi = math.acos(-q_c / (2.0 * r))
            z = 2.0 * ((-p_c / 3.0) ** 0.5) * math.cos(phi / 3.0)

        return z - b_c / 3.0

    def solve(self):
        p, q, r = self.canonical_form()

        # Случай, когда q == 0 (биквадратное уравнение)
        if abs(q) < 1e-11:
            disc_y = p**2 - 4 * r
            y_roots = []
            
            if disc_y >= 0:
                y2_1 = (-p + math.sqrt(disc_y)) / 2.0
                y2_2 = (-p - math.sqrt(disc_y)) / 2.0
                
                for y2 in (y2_1, y2_2):
                    
                    if y2 > 1e-11:
                        y_roots.extend([math.sqrt(y2), -math.sqrt(y2)])
                    elif abs(y2) <= 1e-11:
                        y_roots.append(0.0)

            shift = self.b / (4.0 * self.a)
            return sorted(list(set(round(y - shift, 8) for y in y_roots)))

        # Формируем кубическую резольвенту
        A, B, C, D = self.ferari_resolvent(p, q, r)

        # Находим действительный корень t
        t = self._solve_cubic_real(A, B, C, D)

        # Гарантируем, что 2t - p >= 0 для получения вещественных коэффициентов
        val = 2.0 * t - p
        if val < 0 and abs(val) < 1e-11:
            val = 0.0
        sqrt_2t_p = math.sqrt(val)

        # Разложение на два квадратных уравнения относительно y:
        # y^2 + sqrt(2t - p)*y + (t - q / (2 * sqrt(2t - p))) = 0
        # y^2 - sqrt(2t - p)*y + (t + q / (2 * sqrt(2t - p))) = 0
        k = q / (2.0 * sqrt_2t_p)

        # Коэффициенты c1, c2 для y^2 + b1*y + c1 = 0 и y^2 + b2*y + c2 = 0
        b1, c1 = sqrt_2t_p, t - k
        b2, c2 = -sqrt_2t_p, t + k

        # Дискриминанты двух квадратных уравнений
        d1 = b1**2 - 4.0 * c1
        d2 = b2**2 - 4.0 * c2

        y_roots = []

        # Поиск корней первого уравнения
        if d1 >= 0:
            sqrt_d1 = math.sqrt(d1)
            y_roots.append((-b1 + sqrt_d1) / 2.0)
            if d1 > 0:
                y_roots.append((-b1 - sqrt_d1) / 2.0)

        # Поиск корней второго уравнения
        if d2 >= 0:
            sqrt_d2 = math.sqrt(d2)
            y_roots.append((-b2 + sqrt_d2) / 2.0)
            if d2 > 0:
                y_roots.append((-b2 - sqrt_d2) / 2.0)

        # Обратная подстановка x = y - b / (4a)
        shift = self.b / (4.0 * self.a)
        x_roots = [y - shift for y in y_roots]

        # Убираем дубликаты и округляем погрешности
        unique_roots = []
        for x in x_roots:
            x_rounded = round(x, 8)
            if abs(x_rounded) == 0:
                x_rounded = 0.0
            if x_rounded not in unique_roots:
                unique_roots.append(x_rounded)

        return sorted(unique_roots)

    def print_solution(self):
        roots = self.solve()
        count = len(roots)

        print(f"Количество действительных корней: {count}")
        if count == 0:
            print("Действительных корней нет.")
        else:
            for i, root in enumerate(roots, 1):
                print(f"x{i} = {root}")


if __name__ == "__main__":
    eq = Equation(1, -10, 35, -50, 24) # (корни: 1, 2, 3, 4)
    eq.print_solution()