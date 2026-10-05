import random
import time
from pathlib import Path

MAX_HP = 3000
MIN_HP = 1600

class HP:
    def __init__(self):
        self.max_hp: int = MAX_HP
        self.min_hp: int = MIN_HP
        self.current_hp: float = 0.0
        self.spells_cast = 0
        self.mistakes = 0
        self._last_fight = (14.0, 6, 2)
        self._fight_started_at = time.monotonic()
        self._has_spawned = False
        self._model = None
        self._torch = None
        self._x_min = None
        self._x_max = None
        self._y_min = None
        self._y_max = None
        self._load_model()
        self.reset()

    def take_damage(self, damage: float):
        """Уменьшает текущее здоровье.
        Args:
            damage (float): Количество урона
        """
        self.current_hp = max(0.0, self.current_hp - damage)

    def register_spell_cast(self):
        self.spells_cast += 1

    def register_mistake(self):
        self.mistakes += 1

    def _load_model(self):
        model_path = Path(__file__).resolve().parents[1] / "ml" / "hp_model.pt"
        if not model_path.exists():
            return

        try:
            import torch
            from ml.generate_model import HPRegressionModel

            try:
                checkpoint = torch.load(model_path, map_location="cpu", weights_only=True)
            except TypeError:
                checkpoint = torch.load(model_path, map_location="cpu")

            model = HPRegressionModel(input_dim=3)
            model.load_state_dict(checkpoint["model_state"])
            model.eval()

            self._torch = torch
            self._model = model
            self._x_min = checkpoint["x_min"]
            self._x_max = checkpoint["x_max"]
            self._y_min = checkpoint.get("y_min", torch.tensor(0.0))
            self._y_max = checkpoint.get("y_max", torch.tensor(1.0))
        except (ImportError, OSError, RuntimeError, KeyError, TypeError, ValueError):
            self._model = None

    def generate_hp(self) -> int:
        """Оценивает запас здоровья по результатам прошлого боя."""
        if self._model is not None:
            features = self._torch.tensor([self._last_fight], dtype=self._torch.float32)
            features = self._torch.maximum(self._x_min, self._torch.minimum(features, self._x_max))
            features = (features - self._x_min) / (self._x_max - self._x_min + 1e-8)
            with self._torch.inference_mode():
                prediction = self._model(features).item()
            prediction = prediction * (self._y_max - self._y_min).item() + self._y_min.item()
            return round(max(self.min_hp, min(self.max_hp, prediction)))

        return random.randint(self.min_hp, self.max_hp)

    def reset(self):
        """Создает врага, учитывая результаты предыдущего боя."""
        if self._has_spawned and self.is_dead:
            clear_time = min(25.0, max(3.0, time.monotonic() - self._fight_started_at))
            spells_cast = min(12, max(2, self.spells_cast))
            mistakes = min(5, max(0, self.mistakes))
            self._last_fight = (clear_time, spells_cast, mistakes)

        self.max_hp = self.generate_hp()
        self.current_hp = float(self.max_hp)
        self.spells_cast = 0
        self.mistakes = 0
        self._fight_started_at = time.monotonic()
        self._has_spawned = True

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