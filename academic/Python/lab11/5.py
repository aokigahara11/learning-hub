import sympy as sp
from sympy.polys.polytools import Poly

# Исследование разрешимости уравнений высших степеней (n ≥ 5) в 
# радикалах на основе теории Галуа. 
# Согласно теореме Абеля — Руффини, уравнения степени 5 и выше неразрешимы 
# в радикалах в общем виде. Однако конкретное уравнение может быть решено в 
# радикалах, если его группа Галуа является разрешимой группой. На практике 
# полином, введенный пользователем, может оказаться приводимым 
# (раскладывающимся на множители). В таком случае его разрешимость зависит от 
# разрешимости групп Галуа каждого из его неприводимых множителей.  

class Equation:
    def __init__(self, a5: float, a4: float, a3: float, a2: float, a1: float, a0: float):
        if a5 == 0:
            print("Старший коэффициент 'a5' не может быть равен 0!")
            return
        
        self.coeffs = [float(a5), float(a4), float(a3), float(a2), float(a1), float(a0)]
        self.x = sp.Symbol('x')
        
        self.poly_expr = (
            self.coeffs[0] * self.x**5 +
            self.coeffs[1] * self.x**4 +
            self.coeffs[2] * self.x**3 +
            self.coeffs[3] * self.x**2 +
            self.coeffs[4] * self.x +
            self.coeffs[5]
        )

    def analyze_solvability(self) -> tuple[bool, list]:
        """Анализирует неприводимые множители полинома на разрешимость в радикалах."""
        poly = Poly(self.poly_expr, self.x, domain='Q')
        const_factor, factors_list = poly.factor_list()

        is_solvable = True
        factors_info = []

        for f_poly, pow_val in factors_list:
            deg = f_poly.degree()
            info = {"expr": f_poly.as_expr(), "degree": deg, "solvable": True, "group": None}

            if deg > 4:
                try:
                    galois_grp, _ = f_poly.galois_group()
                    info["group"] = galois_grp
                    if not galois_grp.is_solvable:
                        info["solvable"] = False
                        is_solvable = False
                except Exception:
                    info["solvable"] = False
                    is_solvable = False

            factors_info.append(info)

        return is_solvable, factors_info

    def solve(self) -> dict:
        is_solvable, factors_info = self.analyze_solvability()
        poly = Poly(self.poly_expr, self.x, domain='Q')
        roots = []

        if is_solvable:
            try:
                raw_roots = sp.solve(self.poly_expr, self.x)
                roots = [complex(sp.N(r)) if r.is_complex else float(r) for r in raw_roots]
            except NotImplementedError:
                roots = [complex(r) for r in poly.nroots()]
        else:
            roots = [complex(r) for r in poly.nroots()]

        return {
            "is_solvable": is_solvable,
            "factors": factors_info,
            "roots": roots
        }

    def print_solution(self):
        result = self.solve()

        print("\nРазложение на неприводимые множители и анализ Галуа:")
        for idx, factor in enumerate(result["factors"], 1):
            deg = factor["degree"]
            status = "Разрешим" if factor["solvable"] else "НЕразрешим"
            group_str = f", Группа Галуа: {factor['group']}" if factor["group"] else ""
            print(f"  {idx}. {factor['expr']} (Степень: {deg}{group_str}) -> {status}")

        if result["is_solvable"]:
            print("Уравнение можно решить в радикалах.")
        else:
            print("Уравнение невозможно решить в радикалах в общем виде.")

        print("\nКорни уравнения:")
        for i, root in enumerate(result["roots"], 1):
            if isinstance(root, complex):
                real = round(root.real, 6)
                imag = round(root.imag, 6)
                sign = "+" if imag >= 0 else "-"
                print(f"  x{i} = {real} {sign} {abs(imag)}i")
            else:
                print(f"  x{i} = {round(root, 6)}")


if __name__ == "__main__":
    eq1 = Equation(1, 0, 0, 0, 0, -1) # Разрешимое уравнение
    eq1.print_solution()

    print("\n")

    eq2 = Equation(1, 0, 0, 0, -4, 2) # Неразрешимое уравнение в радикалах
    eq2.print_solution()