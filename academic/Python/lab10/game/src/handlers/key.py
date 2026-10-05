# game/src/handlers/key.py

import pygame
from service.combo import ComboEngine
from service.spells import SpellService
from service.hp import HP


class KeyHandler:

    def __init__(self, combo: ComboEngine, spells: SpellService):
        self.combo = combo
        self.spells = spells

    def handle_event(self, event: pygame.event.Event, hp: HP):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3):
                self._cast_current_spell(hp)

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
                self._cast_current_spell(hp)

    def _cast_current_spell(self, hp: HP):
        """Наносит урон из текущего спелла по объекту HP."""
        spell = self.combo.current_spell
        if not spell:
            return

        spell_name = spell["name"]

        if self.spells.cast_spell(spell_name):
            damage = spell.get("damage", 0)
            hp.take_damage(damage)
            self.combo.reset_spell()
        else:
            rem = self.spells.get_remaining_cooldown(spell_name)
            print(f"Заклинание {spell_name} на перезарядке! (осталось {rem}с)")