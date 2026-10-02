# game/src/main.py

import sys
import pygame
from handlers.key import KeyHandler
from service.combo import ComboEngine
from ui.ui import UI

def main():
    combo_engine = ComboEngine()
    key_handler = KeyHandler(combo_engine)
    ui = UI()

    enemy_hp = 2000.0
    enemy_max_hp = 2000.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            enemy_hp = key_handler.handle_event(event, enemy_hp)

        ui.render(
            enemy_hp=enemy_hp,
            enemy_max_hp=enemy_max_hp,
            active_spheres=combo_engine.spheres,
            current_spell=combo_engine.current_spell,
        )

        ui.clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()