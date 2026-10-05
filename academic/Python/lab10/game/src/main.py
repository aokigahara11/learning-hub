# game/src/main.py

import sys
import pygame
from handlers.key import KeyHandler
from service.combo import ComboEngine
from service.spells import SpellService
from service.hp import HP
from ui.ui import UI

def main():
    combo_engine = ComboEngine()
    spells = SpellService()
    key_handler = KeyHandler(combo_engine, spells)
    ui = UI()
    enemy_hp = HP()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            key_handler.handle_event(event, enemy_hp)

        if enemy_hp.is_dead:
            enemy_hp.reset()
            spells.reset_cooldowns()
            combo_engine.current_spell = None

        ui.render(
            enemy_hp=enemy_hp.current_hp,
            enemy_max_hp=enemy_hp.max_hp,
            active_spheres=combo_engine.spheres,
            current_spell=combo_engine.current_spell,
        )

        ui.clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()