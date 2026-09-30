import sys
import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 165

COLOR = (0, 0, 240)

# 2. Физика шарика 
# Создайте симуляцию физического поведения шара, учитывающего гравитацию, трение и 
# упругость отскоков от стен.

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        # Вектор скорости (px / frame)
        self.vx = 5.0
        self.vy = 0.0

        # Физические параметры
        self.gravity = 0.4
        self.bounce = 0.75
        self.air_friction = 0.998
        self.ground_friction = 0.98

        self.is_grabbed = False


class Backend:
    def __init__(self, ball):
        self.ball = ball

    def update(self, mouse_pos, mouse_buttons):
        ball = self.ball
        mx, my = mouse_pos
        dx = mx - ball.x
        dy = my - ball.y
        distance = (dx**2 + dy**2) ** 0.5

        left_click_held = mouse_buttons[0]

        if (distance <= ball.radius or ball.is_grabbed) and left_click_held:
            ball.is_grabbed = True

            # Плавно следуем за курсором
            new_x = ball.x + dx * 0.2
            new_y = ball.y + dy * 0.2

            # Вычисляем импульс для броска при отпускании ПКМ/ЛКМ
            ball.vx = new_x - ball.x
            ball.vy = new_y - ball.y

            ball.x = new_x
            ball.y = new_y
        else:
            ball.is_grabbed = False

            # Обычная физика падения и полета
            ball.vy += ball.gravity
            ball.vx *= ball.air_friction
            ball.vy *= ball.air_friction

            ball.x += ball.vx
            ball.y += ball.vy

        # Обработка падения на пол
        if ball.y + ball.radius >= SCREEN_HEIGHT:
            ball.y = SCREEN_HEIGHT - ball.radius
            ball.vy *= -ball.bounce
            ball.vx *= ball.ground_friction

            if abs(ball.vy) < 0.5:
                ball.vy = 0

        # Обработка попадания в потолок
        elif ball.y - ball.radius <= 0:
            ball.y = ball.radius
            ball.vy *= -ball.bounce

        # Обработка попадания в правую стену
        if ball.x + ball.radius >= SCREEN_WIDTH:
            ball.x = SCREEN_WIDTH - ball.radius
            ball.vx *= -ball.bounce

        # Обработка попадания в левую стену
        elif ball.x - ball.radius <= 0:
            ball.x = ball.radius
            ball.vx *= -ball.bounce


class Graphics:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Физика шарика")
        self.clock = pygame.time.Clock()

        self.ball = Ball(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            radius=40,
            color=COLOR,
        )
        self.backend = Backend(self.ball)

    def draw_ball(self):
        draw_color = (80, 80, 255) if self.ball.is_grabbed else self.ball.color
        pygame.draw.circle(
            self.screen,
            draw_color,
            (int(self.ball.x), int(self.ball.y)),
            self.ball.radius,
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            self.backend.update(mouse_pos, mouse_buttons)

            self.screen.fill((220, 220, 220))
            self.draw_ball()
            pygame.display.flip()

            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Graphics()
    app.run()