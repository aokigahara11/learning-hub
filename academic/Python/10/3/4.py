import sys
import random
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 165

COLOR_BG = (15, 20, 30)
COLOR_GROUND = (30, 35, 45)
COLOR_RAIN_BASE = (180, 210, 255)

# Имитация дождя 
# Создайте эффект дождя с каплями, падающими сверху вниз, отражающимися от земли. 

class Graphics:
    def __init__(self, screen):
        self.screen = screen

    def draw_background(self, ground_y):
        """Отрисовка фона и интерьера"""
        self.screen.fill(COLOR_BG)

        pygame.draw.rect(
            self.screen, 
            COLOR_GROUND, 
            (0, ground_y, SCREEN_WIDTH, SCREEN_HEIGHT - ground_y)
        )

        pygame.draw.line(
            self.screen, 
            (50, 60, 80), 
            (0, ground_y), 
            (SCREEN_WIDTH, ground_y), 
            2
        )

    def draw_rain(self, drops):
        """Отрисовка капель дождя"""
        for drop in drops:
            # Цвет с учетом прозрачности/яркости для эффекта глубины
            color = (
                int(COLOR_RAIN_BASE[0] * drop['brightness']),
                int(COLOR_RAIN_BASE[1] * drop['brightness']),
                int(COLOR_RAIN_BASE[2] * drop['brightness'])
            )
            
            end_x = drop['x'] + drop['wind'] * 2
            end_y = drop['y'] + drop['length']
            
            pygame.draw.line(
                self.screen, 
                color, 
                (drop['x'], drop['y']), 
                (end_x, end_y), 
                drop['thickness']
            )

    def draw_splashes(self, splashes):
        """Отрисовка всплесков на земле"""
        for splash in splashes:
            alpha_ratio = splash['alpha'] / 255.0
            color = (
                int(COLOR_RAIN_BASE[0] * alpha_ratio),
                int(COLOR_RAIN_BASE[1] * alpha_ratio),
                int(COLOR_RAIN_BASE[2] * alpha_ratio)
            )
            
            rect = pygame.Rect(
                splash['x'] - splash['radius_x'],
                splash['y'] - splash['radius_y'],
                splash['radius_x'] * 2,
                splash['radius_y'] * 2
            )

            pygame.draw.ellipse(self.screen, color, rect, 1)


class Backend:
    def __init__(self):
        self.ground_y = SCREEN_HEIGHT - 80
        self.drop_count = 250
        self.wind = 1.5
        
        self.drops = []
        self.splashes = []
        
        # Первоначальная генерация капель по всему экрану
        for _ in range(self.drop_count):
            self.drops.append(self.create_drop(random_y=True))

    def create_drop(self, random_y=False):
        """Создание одной капли с глубиной"""
        z_factor = random.uniform(0.3, 1.0)
        
        return {
            'x': random.randint(-100, SCREEN_WIDTH + 100),
            'y': random.randint(-SCREEN_HEIGHT, 0) if not random_y else random.randint(0, self.ground_y),
            'speed': 8 * z_factor + 6,
            'length': int(12 * z_factor + 8),
            'thickness': max(1, int(2 * z_factor)),
            'brightness': z_factor,
            'wind': self.wind * z_factor
        }

    def create_splash(self, x, y):
        """Создание всплеска при ударе о землю"""
        self.splashes.append({
            'x': x,
            'y': y,
            'radius_x': 2,
            'radius_y': 1,
            'max_radius': random.randint(6, 14),
            'alpha': 255,
            'fade_speed': 18
        })

    def update(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            drop['x'] += drop['wind']

            # Если капля достигла земли — создаем всплеск и пересоздаем ее сверху
            if drop['y'] >= self.ground_y:
                self.create_splash(drop['x'], self.ground_y + random.randint(-2, 4))
                # Сбрасываем каплю наверх
                new_drop = self.create_drop(random_y=False)
                drop.update(new_drop)

        for splash in self.splashes[:]:
            splash['radius_x'] += 1.2
            splash['radius_y'] += 0.5
            splash['alpha'] -= splash['fade_speed']

            if splash['alpha'] <= 0 or splash['radius_x'] >= splash['max_radius']:
                self.splashes.remove(splash)


class Game:
    """Главный контроллер симуляции"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Симуляция дождя с эффектом всплесков")
        self.clock = pygame.time.Clock()

        self.backend = Backend()
        self.graphics = Graphics(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Обновление физики дождя
            self.backend.update()

            # Отрисовка кадра
            self.graphics.draw_background(self.backend.ground_y)
            self.graphics.draw_splashes(self.backend.splashes)
            self.graphics.draw_rain(self.backend.drops)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()