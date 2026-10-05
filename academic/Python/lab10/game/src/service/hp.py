import random

MAX_HP = 3000
MIN_HP = 1600

class HP:
    def __init__(self):
        self.max_hp: int = MAX_HP
        self.min_hp: int = MIN_HP
        self.current_hp: float = 0.0
        self.reset()

    def take_damage(self, damage: float):
        """Уменьшает текущее здоровье.
        Args:
            damage (float): Количество урона
        """
        self.current_hp = max(0.0, self.current_hp - damage)

    def generate_hp(self) -> int:
        """Генерирует случайный случайный запас здоровья в диапазоне [MIN_HP, MAX_HP]."""
        return random.randint(self.min_hp, self.max_hp)

    def reset(self):
        """Спавнит нового врага со случайным количеством HP."""
        self.max_hp = self.generate_hp()
        self.current_hp = float(self.max_hp)

    @property
    def is_dead(self) -> bool:
        """Проверка, обнулилось ли здоровье."""
        return self.current_hp <= 0.0

    @property
    def ratio(self) -> float:
        """Возвращает процент оставшегося здоровья (0.0 - 1.0) для UI полоски."""
        if self.max_hp == 0:
            return 0.0
        return self.current_hp / self.max_hp