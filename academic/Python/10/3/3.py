import sys
import math
import random
import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 165

RIVER_LENGTH = 2000 

COLOR_WATER = (30, 110, 190)
COLOR_WAVE = (60, 140, 220)
COLOR_BANK = (34, 139, 34)
COLOR_FINISH = (218, 165, 32)
COLOR_BOAT = (139, 69, 19)
COLOR_LOG = (101, 67, 33)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (220, 50, 50)

# 3. Мини-игра "Переправься через реку" 
# Игрок управляет лодкой, пересекающей реку с течением воды и препятствиями. 

class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.wave_offset = 0.0

    def draw_world(self, camera_y, river_length, river_current):
        """Отрисовка обьектов игры"""
        self.screen.fill(COLOR_WATER)

        # Отрисовка волн с учетом камеры
        self.wave_offset += river_current * 1.5
        for y in range(0, SCREEN_HEIGHT + 40, 50):
            world_y = y + camera_y
            
            # Рисуем волны только в пределах реки
            if 0 <= world_y <= river_length:
                for x in range(0, SCREEN_WIDTH + 40, 60):
                    wave_x = (x + self.wave_offset) % (SCREEN_WIDTH + 60) - 30
                    wave_y = y + math.sin((x + self.wave_offset) * 0.03) * 4
                    pygame.draw.arc(
                        self.screen, COLOR_WAVE,
                        (wave_x, wave_y, 40, 15),
                        0, math.pi, 2
                    )

        # Берег (Старт)
        start_bank_screen_y = river_length - camera_y
        if start_bank_screen_y < SCREEN_HEIGHT:
            pygame.draw.rect(
                self.screen, COLOR_BANK,
                (0, start_bank_screen_y, SCREEN_WIDTH, SCREEN_HEIGHT)
            )

        # Берег (Финиш)
        finish_bank_screen_y = 0 - camera_y
        if finish_bank_screen_y + 100 > 0:
            pygame.draw.rect(
                self.screen, COLOR_FINISH,
                (0, finish_bank_screen_y - 300, SCREEN_WIDTH, 300)
            )

    def draw_boat(self, boat_x, boat_y, camera_y, width=26, height=44):
        """Отрисовка лодки"""
        screen_y = boat_y - camera_y

        boat_rect = pygame.Rect(boat_x - width // 2, screen_y - height // 2, width, height)
        pygame.draw.rect(self.screen, COLOR_BOAT, boat_rect, border_radius=6)

        nose_points = [
            (boat_x - width // 2, screen_y - height // 2),
            (boat_x + width // 2, screen_y - height // 2),
            (boat_x, screen_y - height // 2 - 12)
        ]

        pygame.draw.polygon(self.screen, COLOR_BOAT, nose_points)

    def draw_obstacles(self, obstacles, camera_y):
        """Отрисовка брёвен (препятствия)"""
        for obs in obstacles:
            screen_y = obs['y'] - camera_y
            # Рисуем только те объекты, которые попадают в экран
            if -50 <= screen_y <= SCREEN_HEIGHT + 50:
                rect = pygame.Rect(obs['x'], screen_y, obs['w'], obs['h'])
                pygame.draw.rect(self.screen, COLOR_LOG, rect, border_radius=4)

    def draw_ui(self, lives, distance_left, is_won, is_game_over):
        """Отрисовка интерфейса игры"""
        lives_text = self.font.render(f"Жизни: {lives}", True, COLOR_WHITE)
        self.screen.blit(lives_text, (15, 15))

        dist_text = self.font.render(f"Осталось: {int(distance_left)}px", True, COLOR_WHITE)
        self.screen.blit(dist_text, (SCREEN_WIDTH - 195, 15))

        if is_won:
            win_text = self.font.render("ФИНИШ ДОСТИГНУТ! (R — рестарт)", True, COLOR_WHITE)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2))
        elif is_game_over:
            over_text = self.font.render("ЛОДКА РАЗБИТА! (R — рестарт)", True, COLOR_RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2))


class Backend:
    def __init__(self):
        self.reset()

    def reset(self):
        self.boat_x = SCREEN_WIDTH // 2
        self.boat_y = RIVER_LENGTH - 40
        self.boat_speed = 3.5

        self.river_current = 1.2
        self.lives = 3
        self.is_won = False
        self.is_game_over = False

        self.camera_y = self.boat_y - SCREEN_HEIGHT + 150

        self.obstacles = []
        self.generate_initial_obstacles()

    def generate_initial_obstacles(self):
        """Генерация брёвен по всей длине реки от старта до финиша"""
        for y in range(100, RIVER_LENGTH - 150, 70):
            if random.random() < 0.4:
                w = random.randint(60, 110)
                h = 18
                x = random.randint(0, SCREEN_WIDTH - w)
                speed = random.uniform(1.0, 3.0) * (1 if random.random() > 0.5 else -1)
                self.obstacles.append({'x': x, 'y': y, 'w': w, 'h': h, 'speed': speed})

    def update(self, keys):
        if self.is_won or self.is_game_over:
            return

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.boat_y -= self.boat_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.boat_y += self.boat_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.boat_x -= self.boat_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.boat_x += self.boat_speed

        self.boat_x += self.river_current

        self.boat_x = max(15, min(SCREEN_WIDTH - 15, self.boat_x))
        self.boat_y = min(RIVER_LENGTH - 20, self.boat_y)

        target_camera_y = self.boat_y - SCREEN_HEIGHT + 200
        self.camera_y = max(-100, min(RIVER_LENGTH - SCREEN_HEIGHT + 100, target_camera_y))

        for obs in self.obstacles:
            obs['x'] += obs['speed']
            if obs['x'] <= 0 or obs['x'] + obs['w'] >= SCREEN_WIDTH:
                obs['speed'] *= -1

        boat_hitbox = pygame.Rect(self.boat_x - 10, self.boat_y - 18, 20, 36)
        for obs in self.obstacles[:]:
            obs_rect = pygame.Rect(obs['x'], obs['y'], obs['w'], obs['h'])
            if boat_hitbox.colliderect(obs_rect):
                self.obstacles.remove(obs)
                self.lives -= 1
                if self.lives <= 0:
                    self.is_game_over = True

        if self.boat_y <= 0:
            self.is_won = True

    def get_distance_left(self):
        return max(0, self.boat_y)


class Game:
    """Контроллер игры"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Переправься через реку")
        self.clock = pygame.time.Clock()

        self.backend = Backend()
        self.graphics = Graphics(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.backend.reset()

            keys_pressed = pygame.key.get_pressed()
            self.backend.update(keys_pressed)

            # Рендеринг с учётом camera_y
            self.graphics.draw_world(
                self.backend.camera_y,
                RIVER_LENGTH,
                self.backend.river_current
            )
            self.graphics.draw_obstacles(
                self.backend.obstacles, 
                self.backend.camera_y
            )
            self.graphics.draw_boat(
                self.backend.boat_x, 
                self.backend.boat_y, 
                self.backend.camera_y
            )
            self.graphics.draw_ui(
                self.backend.lives,
                self.backend.get_distance_left(),
                self.backend.is_won,
                self.backend.is_game_over
            )

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()