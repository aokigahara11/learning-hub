import sys
import math
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 165

COLOR_BG = (30, 35, 45)
COLOR_PLAYER = (52, 152, 219)
COLOR_ENEMY_PATROL = (241, 196, 15)
COLOR_ENEMY_CHASE = (231, 76, 60)
COLOR_WAYPOINT = (149, 165, 166)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (220, 50, 50)


class Graphics:
    """Визуализация игрока, ИИ врага, радиусов и UI"""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def draw_background(self):
        self.screen.fill(COLOR_BG)

    def draw_waypoints(self, waypoints):
        """Отрисовка маршрута патрулирования"""
        for i, pt in enumerate(waypoints):
            pygame.draw.circle(self.screen, COLOR_WAYPOINT, (int(pt[0]), int(pt[1])), 5)
            next_pt = waypoints[(i + 1) % len(waypoints)]
            pygame.draw.line(self.screen, (50, 60, 75), pt, next_pt, 1)

    def draw_player(self, x, y, radius=18):
        pygame.draw.circle(self.screen, COLOR_PLAYER, (int(x), int(y)), radius)

    def draw_enemy(self, enemy):
        """Отрисовка врага с радиусами обнаружения"""
        x, y = int(enemy.x), int(enemy.y)
        
        detection_color = (231, 76, 60, 40) if enemy.state == "CHASE" else (241, 196, 15, 30)
        radius_surface = pygame.Surface((enemy.detection_radius * 2, enemy.detection_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            radius_surface, 
            detection_color, 
            (enemy.detection_radius, enemy.detection_radius), 
            enemy.detection_radius
        )
        self.screen.blit(radius_surface, (x - enemy.detection_radius, y - enemy.detection_radius))

        color = COLOR_ENEMY_CHASE if enemy.state == "CHASE" else COLOR_ENEMY_PATROL
        pygame.draw.circle(self.screen, color, (x, y), enemy.radius)

    def draw_ui(self, enemy_state, survival_time, is_caught, is_won):
        """Отрисовка статуса ИИ и таймера выживания"""
        state_text_val = "ПРЕСЛЕДОВАНИЕ!" if enemy_state == "CHASE" else "ПАТРУЛИРОВАНИЕ"
        state_color = COLOR_ENEMY_CHASE if enemy_state == "CHASE" else COLOR_ENEMY_PATROL
        
        ui_state = self.font.render(f"ИИ Врага: {state_text_val}", True, state_color)
        self.screen.blit(ui_state, (20, 20))

        timer_text = self.font.render(f"Продержаться: {max(0, int(survival_time))} сек", True, COLOR_WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 240, 20))

        if is_caught:
            over_text = self.font.render("ПОЙМАН! (Нажмите R для сброса)", True, COLOR_RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2))
        elif is_won:
            win_text = self.font.render("ВЫ УБЕЖАЛИ ОТ ИИ! ПОБЕДА! (R - сброс)", True, COLOR_PLAYER)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))


class EnemyAI:
    """Класс противника с конечным автоматом (FSM)"""

    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.current_wp_index = 0
        
        self.x = waypoints[0][0]
        self.y = waypoints[0][1]
        self.radius = 20

        self.patrol_speed = 3.0
        self.chase_speed = 5.0
        self.detection_radius = 180
        self.chase_loss_radius = 280

        self.state = "PATROL"

    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist_to_player = math.hypot(dx, dy)

        # 2. Логика переключения состояний
        if self.state == "PATROL":
            if dist_to_player <= self.detection_radius:
                self.state = "CHASE"
        
        elif self.state == "CHASE":
            if dist_to_player > self.chase_loss_radius:
                self.state = "PATROL"

        if self.state == "PATROL":
            target_wp = self.waypoints[self.current_wp_index]
            wp_dx = target_wp[0] - self.x
            wp_dy = target_wp[1] - self.y
            dist_to_wp = math.hypot(wp_dx, wp_dy)

            # Переключение на следующую путевую точку
            if dist_to_wp < 5:
                self.current_wp_index = (self.current_wp_index + 1) % len(self.waypoints)
            else:
                # Движение к путевой точке
                self.x += (wp_dx / dist_to_wp) * self.patrol_speed
                self.y += (wp_dy / dist_to_wp) * self.patrol_speed

        elif self.state == "CHASE":
            if dist_to_player > 0:
                self.x += (dx / dist_to_player) * self.chase_speed
                self.y += (dy / dist_to_player) * self.chase_speed


class Backend:
    """Бэкенд: Логика игрока, таймеры и проверка поимки"""

    def __init__(self):
        self.waypoints = [
            (150, 150),
            (650, 150),
            (650, 450),
            (150, 450)
        ]
        self.reset()

    def reset(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = 530
        self.player_speed = 4.0
        self.player_radius = 16

        self.enemy = EnemyAI(self.waypoints)
        self.survival_time = 30.0 # Время выживания (секунды)
        
        self.is_caught = False
        self.is_won = False

    def update(self, keys, dt):
        if self.is_caught or self.is_won:
            return

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_y -= self.player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_y += self.player_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_x -= self.player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_x += self.player_speed

        self.player_x = max(self.player_radius, min(SCREEN_WIDTH - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius, min(SCREEN_HEIGHT - self.player_radius, self.player_y))

        self.enemy.update(self.player_x, self.player_y)

        dist_to_enemy = math.hypot(self.player_x - self.enemy.x, self.player_y - self.enemy.y)
        if dist_to_enemy <= (self.player_radius + self.enemy.radius):
            self.is_caught = True

        self.survival_time -= dt
        if self.survival_time <= 0:
            self.survival_time = 0
            self.is_won = True


class Game:
    """Контроллер игры"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Интеллект врага: Патруль и Преследование")
        self.clock = pygame.time.Clock()

        self.backend = Backend()
        self.graphics = Graphics(self.screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.backend.reset()

            keys_pressed = pygame.key.get_pressed()
            self.backend.update(keys_pressed, dt)

            self.graphics.draw_background()
            self.graphics.draw_waypoints(self.backend.waypoints)
            self.graphics.draw_enemy(self.backend.enemy)
            self.graphics.draw_player(self.backend.player_x, self.backend.player_y)
            self.graphics.draw_ui(
                self.backend.enemy.state,
                self.backend.survival_time,
                self.backend.is_caught,
                self.backend.is_won
            )

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()