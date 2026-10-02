# game/src/handlers/key_handler.py

import pygame
from service.combo import ComboEngine

class KeyHandler:

    def __init__(self, combo: ComboEngine):
        self.combo = combo

    def handle_event(self, event: pygame.event.Event, enemy_hp: float) -> float:
        """Обрабатывает события клавиш и мыши.
        Returns:
            float: Обновленное значение HP врага.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3):
                enemy_hp = self._cast_current_spell(enemy_hp)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.combo.add_sphere("Q")
            elif event.key == pygame.K_w:
                self.combo.add_sphere("W")
            elif event.key == pygame.K_e:
                self.combo.add_sphere("E")

            elif event.key == pygame.K_r:
                self.combo.invoke()

            elif event.key in (pygame.K_d, pygame.K_f, pygame.K_SPACE):
                enemy_hp = self._cast_current_spell(enemy_hp)

        return enemy_hp

    def _cast_current_spell(self, enemy_hp: float) -> float:
        """Наносит урон из текущего спелла по врагу."""
        spell = self.combo.current_spell
        if not spell:
            return enemy_hp

        damage = spell.get("damage", 0)
        return max(0.0, enemy_hp - damage)