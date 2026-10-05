# src/service/spells.py
import pygame
from database.database import DatabaseSpells

class SpellService:
    def __init__(self, cooldown_ms: int = 15000, max_active_spells: int = 8):
        self.cooldown_ms = cooldown_ms
        self.max_active_spells = max_active_spells
        self.used_spells: dict[str, int] = {}

    def _cleanup_expired(self, now: int):
        """Вспомогательный метод: удаляет спеллы, у которых уже истек кулдаун."""
        expired = [
            name
            for name, time_cast in self.used_spells.items()
            if now - time_cast >= self.cooldown_ms
        ]
        for name in expired:
            del self.used_spells[name]

    def can_cast(self, spell_name: str) -> bool:
        """Проверяет, можно ли кастовать спелл (без записи в словарь)."""
        now = pygame.time.get_ticks()

        if spell_name not in self.used_spells:
            return True

        elapsed = now - self.used_spells[spell_name]
        return elapsed >= self.cooldown_ms

    def cast_spell(self, spell_name: str) -> bool:
        """Регистрирует каст заклинания и обновляет КД других спеллов.
        Returns:
            bool: True если каст успешен, False если спелл на КД.
        """
        now = pygame.time.get_ticks()

        self._cleanup_expired(now)

        if not self.can_cast(spell_name):
            return False

        if len(self.used_spells) >= self.max_active_spells:
            oldest_spell = next(iter(self.used_spells))
            del self.used_spells[oldest_spell]

        self.used_spells[spell_name] = now
        return True

    def get_remaining_cooldown(self, spell_name: str) -> float:
        """Возвращает оставшееся время КД в секундах (для UI)."""
        if spell_name not in self.used_spells:
            return 0.0

        now = pygame.time.get_ticks()
        elapsed = now - self.used_spells[spell_name]
        remaining = (self.cooldown_ms - elapsed) / 1000.0

        if remaining <= 0:
            del self.used_spells[spell_name]
            return 0.0

        return round(remaining, 1)

    def reset_cooldowns(self):
        """Сбрасывает кулдауны всех заклинаний (при смерти врага)."""
        self.used_spells.clear()

    @staticmethod
    def get_spell_by_combo(combo: str) -> dict | None:
        """Ищет спелл в БД по отсортированной комбинации сфер
        Args:
            combo (str): Комбинация из 3 сфер
        Returns:
            dict | None: Словарь с данными спелла или None
        """
        sorted_combo = "".join(sorted(combo.upper()))

        spells = DatabaseSpells.get_all_spells()
        for spell in spells:
            if "".join(sorted(spell["combo"].upper())) == sorted_combo:
                return spell

        return None