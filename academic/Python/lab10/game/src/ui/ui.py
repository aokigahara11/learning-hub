# game/src/ui/ui.py

import os
import sys
import pygame


class UI:
    def __init__(self, window_size=(900, 650)):
        pygame.init()
        pygame.font.init()

        self.width, self.height = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Invoker Game")
        self.clock = pygame.time.Clock()

        self.COLOR_BG = (15, 16, 22)
        self.COLOR_PANEL = (24, 26, 36)
        self.COLOR_BORDER = (45, 50, 68)
        self.COLOR_TEXT = (220, 225, 235)
        self.COLOR_TEXT_MUTED = (120, 128, 145)

        self.COLOR_HP_FILL = (210, 45, 45)
        self.COLOR_HP_BG = (50, 20, 20)

        self.font_main = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 12)

        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.sphere_images = {}
        self.sphere_images_small = {}
        self.spell_images = {}

        self._load_spheres()
        self._load_spells()

    def _load_spheres(self):
        """Загрузка и масштабирование сфер"""
        spheres_map = {
            "Q": "invoker_quas.webp",
            "W": "invoker_wex.webp",
            "E": "invoker_exort.webp",
        }

        for key, filename in spheres_map.items():
            path = os.path.join(self.assets_dir, "spheres", filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.sphere_images[key] = pygame.transform.smoothscale(
                    img, (56, 56)
                )
                self.sphere_images_small[key] = pygame.transform.smoothscale(
                    img, (36, 36)
                )
            else:
                self.sphere_images[key] = None
                self.sphere_images_small[key] = None

    def _load_spells(self):
        """Маппинг имен заклинаний из БД на файлы"""
        spells_map = {
            "Alacrity": "invoker_alacrity.webp",
            "Chaos Meteor": "invoker_chaos_meteor.webp",
            "Cold Snap": "invoker_cold_snap.webp",
            "Deafening Blast": "invoker_deafening_blast.webp",
            "EMP": "invoker_emp.webp",
            "Forge Spirit": "invoker_forge_spirit.webp",
            "Ghost Walk": "invoker_ghost_walk.webp",
            "Ice Wall": "invoker_ice_wall.webp",
            "Invoke": "invoker_invoke.webp",
            "Sun Strike": "invoker_sun_strike.webp",
            "Tornado": "invoker_tornado.webp",
            "empty": "invoker_empty1.webp",
        }

        for name, filename in spells_map.items():
            path = os.path.join(self.assets_dir, "spells", filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.spell_images[name] = pygame.transform.smoothscale(
                    img, (68, 68)
                )
            else:
                self.spell_images[name] = None

    def draw_enemy_hp(
        self,
        current_hp: float,
        max_hp: float,
        enemy_name: str = "ENEMY",
    ):
        center_x = self.width // 2
        center_y = self.height // 2 - 40

        bar_width = 500
        bar_height = 32
        bar_x = center_x - bar_width // 2
        bar_y = center_y

        name_surf = self.font_title.render(enemy_name, True, self.COLOR_TEXT)
        name_rect = name_surf.get_rect(center=(center_x, bar_y - 20))
        self.screen.blit(name_surf, name_rect)

        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(
            self.screen, self.COLOR_HP_BG, bg_rect, border_radius=6
        )

        pct = max(0.0, min(1.0, current_hp / max_hp)) if max_hp > 0 else 0
        fill_width = int(bar_width * pct)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            pygame.draw.rect(
                self.screen, self.COLOR_HP_FILL, fill_rect, border_radius=6
            )

        pygame.draw.rect(
            self.screen, self.COLOR_BORDER, bg_rect, width=2, border_radius=6
        )

        hp_str = f"{int(current_hp)} / {int(max_hp)}"
        hp_surf = self.font_main.render(hp_str, True, (255, 255, 255))
        hp_rect = hp_surf.get_rect(center=(center_x, bar_y + bar_height // 2))
        self.screen.blit(hp_surf, hp_rect)

    def _draw_floating_spheres(self, active_spheres: list[str], hud_y: int, center_x: int):
        """Отрисовывает 3 активные сферы над основной панелью интерфейса"""
        if not active_spheres:
            return

        sphere_size = 36
        spacing = 10
        total_width = (
            len(active_spheres) * sphere_size
            + (len(active_spheres) - 1) * spacing
        )

        start_x = center_x - total_width // 2
        top_y = hud_y - sphere_size - 12

        for i, s_type in enumerate(active_spheres):
            x = start_x + i * (sphere_size + spacing)

            pygame.draw.circle(
                self.screen,
                (20, 22, 32),
                (x + sphere_size // 2, top_y + sphere_size // 2),
                sphere_size // 2 + 3,
            )
            pygame.draw.circle(
                self.screen,
                self.COLOR_BORDER,
                (x + sphere_size // 2, top_y + sphere_size // 2),
                sphere_size // 2 + 3,
                width=1,
            )

            img = self.sphere_images_small.get(s_type)
            if img:
                self.screen.blit(img, (x, top_y))
            else:
                txt = self.font_small.render(s_type, True, (255, 255, 255))
                self.screen.blit(txt, (x + 12, top_y + 8))

    def spells(self, active_spheres: list[str], current_spell: dict | None = None):
        """Отрисовка нижнего HUD: фиксированные сферы Q/W/E и активный спелл."""
        hud_height = 130
        hud_y = self.height - hud_height - 20
        center_x = self.width // 2

        self._draw_floating_spheres(active_spheres, hud_y, center_x)

        hud_rect = pygame.Rect(center_x - 320, hud_y, 640, hud_height)
        
        pygame.draw.rect(self.screen, self.COLOR_PANEL, hud_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, hud_rect, width=2, border_radius=12)

        spheres_title = self.font_small.render(
            "СФЕРЫ (Q / W / E)", True, self.COLOR_TEXT_MUTED
        )
        self.screen.blit(spheres_title, (center_x - 280, hud_y + 12))

        fixed_spheres = ["Q", "W", "E"]
        for i, s_type in enumerate(fixed_spheres):
            slot_x = center_x - 280 + i * 68
            slot_y = hud_y + 38
            slot_rect = pygame.Rect(slot_x, slot_y, 56, 56)

            # Пустой слот-рамка
            pygame.draw.rect(
                self.screen, (18, 20, 28), slot_rect, border_radius=8
            )

            img = self.sphere_images.get(s_type)
            if img:
                self.screen.blit(img, (slot_x, slot_y))
            else:
                txt = self.font_main.render(s_type, True, (255, 255, 255))
                self.screen.blit(
                    txt, txt.get_rect(center=slot_rect.center)
                )

            pygame.draw.rect(
                self.screen,
                self.COLOR_BORDER,
                slot_rect,
                width=1,
                border_radius=8,
            )

        spell_title = self.font_small.render("АКТИВНОЕ ЗАКЛИНАНИЕ (D / F)", True, self.COLOR_TEXT_MUTED)
        self.screen.blit(spell_title, (center_x + 60, hud_y + 12))

        slot_x = center_x + 60
        slot_y = hud_y + 32
        spell_rect = pygame.Rect(slot_x, slot_y, 68, 68)

        pygame.draw.rect(
            self.screen, (18, 20, 28), spell_rect, border_radius=8
        )

        spell_name = current_spell.get("name") if current_spell else None
        img = self.spell_images.get(spell_name) if spell_name else None

        if not img:
            img = self.spell_images.get("empty")

        if img:
            self.screen.blit(img, (slot_x, slot_y))

        pygame.draw.rect(
            self.screen,
            self.COLOR_BORDER,
            spell_rect,
            width=2,
            border_radius=8,
        )

        if current_spell:
            display_name = current_spell.get("name", "")
            combo_str = f"[{current_spell.get('combo', '')}]"

            name_surf = self.font_main.render(
                display_name, True, (255, 215, 0)
            )
            combo_surf = self.font_small.render(
                combo_str, True, self.COLOR_TEXT_MUTED
            )

            self.screen.blit(name_surf, (slot_x + 80, slot_y + 10))
            self.screen.blit(combo_surf, (slot_x + 80, slot_y + 35))
        else:
            none_surf = self.font_main.render(
                "Нет заклинания", True, self.COLOR_TEXT_MUTED
            )
            self.screen.blit(none_surf, (slot_x + 80, slot_y + 22))

    def render(self, enemy_hp: float, enemy_max_hp: float, active_spheres: list[str], current_spell: dict | None = None):
        """Главный метод отрисовки кадра"""
        self.screen.fill(self.COLOR_BG)

        self.draw_enemy_hp(enemy_hp, enemy_max_hp)

        self.spells(active_spheres, current_spell)

        pygame.display.flip()
