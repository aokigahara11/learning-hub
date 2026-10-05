# game/src/service/combo.py
from service.spells import SpellService

class ComboEngine:
    def __init__(self):
        self.spheres: list[str] = []
        self.current_spell: dict | None = None

    def add_sphere(self, sphere: str):
        """Добавляет сферу (Q, W, E) в очередь.
        Если уже есть 3 сферы, удаляет самую старую.
        """
        sphere = sphere.upper()
        if sphere in ("Q", "W", "E"):
            self.spheres.append(sphere)
            if len(self.spheres) > 3:
                self.spheres.pop(0)

    def invoke(self) -> dict | None:
        """Превращает 3 текущие сферы в заклинание."""
        if len(self.spheres) < 3:
            return None

        combo_str = "".join(self.spheres)
        spell = SpellService.get_spell_by_combo(combo_str)

        self.current_spell = spell
        return self.current_spell

    def reset_spell(self):
        """Очищает заинвоканный спелл"""
        self.current_spell = None