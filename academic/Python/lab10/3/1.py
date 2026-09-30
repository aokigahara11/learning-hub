import random
import sys
import pygame

CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS = 165

BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
GRAY = (50, 50, 50)
RED = (220, 50, 50)

SHAPE_COLORS = [
    (0, 240, 240),
    (240, 240, 0),
    (160, 0, 240),
    (240, 160, 0),
    (0, 0, 240),
    (0, 240, 0),
    (240, 0, 0),
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
]


class Block:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape = [row[:] for row in SHAPES[shape_index]]
        self.color = SHAPE_COLORS[shape_index]

    def rotate(self):
        """Поворот фигуры на 90 градусов по часовой стрелке"""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Backend:
    """Игровая логика, математика сетки и обработка коллизий"""

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.grid = [
            [(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)
        ]
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500
        self.current_block = self.new_block()

    def new_block(self):
        """Создание новой фигуры вверху по центру"""
        shape_index = random.randint(0, len(SHAPES) - 1)
        return Block(GRID_WIDTH // 2 - 1, 0, shape_index)

    def valid_move(self, block, offset_x=0, offset_y=0, shape=None):
        """Проверка: корректна ли позиция фигуры в сетке"""
        if shape is None:
            shape = block.shape

        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    new_x = block.x + c + offset_x
                    new_y = block.y + r + offset_y

                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False

                    if new_y >= 0 and self.grid[new_y][new_x] != (0, 0, 0):
                        return False
        return True

    def lock_block(self):
        """Закрепление фигуры в сетке при достижении дна"""
        for r, row in enumerate(self.current_block.shape):
            for c, val in enumerate(row):
                if val:
                    y = self.current_block.y + r
                    x = self.current_block.x + c
                    if y >= 0:
                        self.grid[y][x] = self.current_block.color

        self.clear_lines()
        self.current_block = self.new_block()

        if not self.valid_move(self.current_block):
            self.game_over = True

    def clear_lines(self):
        """Проверка и удаление заполненных линий"""
        new_grid = [
            row for row in self.grid if any(cell == (0, 0, 0) for cell in row)
        ]
        lines_cleared = GRID_HEIGHT - len(new_grid)

        for _ in range(lines_cleared):
            new_grid.insert(0, [(0, 0, 0) for _ in range(GRID_WIDTH)])

        self.grid = new_grid

    def move_left(self):
        if not self.game_over and self.valid_move(
            self.current_block, offset_x=-1
        ):
            self.current_block.x -= 1

    def move_right(self):
        if not self.game_over and self.valid_move(
            self.current_block, offset_x=1
        ):
            self.current_block.x += 1

    def move_down(self):
        if not self.game_over and self.valid_move(
            self.current_block, offset_y=1
        ):
            self.current_block.y += 1

    def rotate_block(self):
        if not self.game_over:
            rotated_shape = [
                list(row) for row in zip(*self.current_block.shape[::-1])
            ]
            if self.valid_move(self.current_block, shape=rotated_shape):
                self.current_block.rotate()

    def update(self, delta_time):
        """Обновление игровой логики"""
        if self.game_over:
            return

        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if self.valid_move(self.current_block, offset_y=1):
                self.current_block.y += 1
            else:
                self.lock_block()


class Graphics:
    """Визуализация, окно и обработка событий ввода"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Падение блоков (Тетрис)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.backend = Backend()

    def handle_input(self):
        """Обработка событий клавиатуры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.backend.game_over:
                    if event.key == pygame.K_r:
                        self.backend.reset_game()
                    return

                if event.key == pygame.K_LEFT:
                    self.backend.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.backend.move_right()
                elif event.key == pygame.K_DOWN:
                    self.backend.move_down()
                elif event.key in (pygame.K_UP, pygame.K_SPACE):
                    self.backend.rotate_block()

    def draw(self):
        """Отрисовка кадра"""
        self.screen.fill(BLACK)

        # Отрисовка уложенных блоков в сетке
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                color = self.backend.grid[r][c]
                rect = pygame.Rect(
                    c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE
                )
                if color != (0, 0, 0):
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

        # Отрисовка текущей падающей фигуры
        if not self.backend.game_over and self.backend.current_block:
            block = self.backend.current_block
            for r, row in enumerate(block.shape):
                for c, val in enumerate(row):
                    if val:
                        x = (block.x + c) * CELL_SIZE
                        y = (block.y + r) * CELL_SIZE
                        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, block.color, rect)
                        pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Отрисовка если игра окончена
        if self.backend.game_over:
            over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Нажмите R", True, WHITE)

            over_rect = over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            )
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            )

            self.screen.blit(over_text, over_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        while True:
            delta_time = self.clock.tick(FPS)
            self.handle_input()
            self.backend.update(delta_time)
            self.draw()


if __name__ == "__main__":
    game = Graphics()
    game.run()