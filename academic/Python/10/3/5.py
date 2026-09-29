import sys
import random
import pygame

GRID_COLS = 21
GRID_ROWS = 21

CELL_SIZE = 30
SCREEN_WIDTH = GRID_COLS * CELL_SIZE
SCREEN_HEIGHT = GRID_ROWS * CELL_SIZE + 50

FPS = 165

COLOR_BG = (25, 25, 30)
COLOR_WALL = (45, 55, 72)
COLOR_PATH = (220, 225, 230)
COLOR_START = (46, 204, 113)
COLOR_FINISH = (231, 76, 60)
COLOR_PLAYER = (52, 152, 219)
COLOR_WHITE = (255, 255, 255)

class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def draw_maze(self, grid, start_pos, finish_pos):
        """Отрисовка стенок, проходов, старта и финиша"""
        self.screen.fill(COLOR_BG)

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                rect = pygame.Rect(
                    c * CELL_SIZE, 
                    r * CELL_SIZE + 50, 
                    CELL_SIZE, 
                    CELL_SIZE
                )
                
                # 1 — Стенка, 0 — Проход
                if grid[r][c] == 1:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_PATH, rect)

        start_rect = pygame.Rect(
            start_pos[1] * CELL_SIZE + 4, 
            start_pos[0] * CELL_SIZE + 54, 
            CELL_SIZE - 8, 
            CELL_SIZE - 8
        )
        pygame.draw.rect(self.screen, COLOR_START, start_rect, border_radius=4)

        finish_rect = pygame.Rect(
            finish_pos[1] * CELL_SIZE + 4, 
            finish_pos[0] * CELL_SIZE + 54, 
            CELL_SIZE - 8, 
            CELL_SIZE - 8
        )
        pygame.draw.rect(self.screen, COLOR_FINISH, finish_rect, border_radius=4)

    def draw_player(self, player_r, player_c):
        """Отрисовка круга игрока"""
        center_x = player_c * CELL_SIZE + CELL_SIZE // 2
        center_y = player_r * CELL_SIZE + 50 + CELL_SIZE // 2
        radius = CELL_SIZE // 3
        pygame.draw.circle(self.screen, COLOR_PLAYER, (center_x, center_y), radius)

    def draw_ui(self, is_won):
        """Интерфейс"""
        pygame.draw.rect(self.screen, COLOR_BG, (0, 0, SCREEN_WIDTH, 50))
        
        info_text = self.font.render("Управление: Стрелки / WASD | R — Новый лабиринт", True, COLOR_WHITE)
        self.screen.blit(info_text, (15, 12))

        if is_won:
            win_text = self.font.render("ЛАБИРИНТ ПРОЙДЕН! (R - повтор)", True, COLOR_START)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))

class Backend:
    def __init__(self):
        self.start_pos = (1, 1)
        self.finish_pos = (GRID_ROWS - 2, GRID_COLS - 2)
        self.reset()

    def reset(self):
        """Генерация нового лабиринта"""
        # 1 — Стенка, 0 — Проход
        self.grid = [[1 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.generate_maze_dfs(self.start_pos[0], self.start_pos[1])
        
        # Гарантируем, что финиш открыт
        self.grid[self.finish_pos[0]][self.finish_pos[1]] = 0

        self.player_r, self.player_c = self.start_pos
        self.is_won = False

    def generate_maze_dfs(self, start_r, start_c):
        """Алгоритм генерации лабиринта"""
        stack = [(start_r, start_c)]
        self.grid[start_r][start_c] = 0

        # Возможные направления шага через 2 ячейки
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            r, c = stack[-1]
            neighbors = []

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Проверяем границы сетки
                if 0 < nr < GRID_ROWS - 1 and 0 < nc < GRID_COLS - 1:
                    if self.grid[nr][nc] == 1:  # Непосещенная ячейка-стена
                        neighbors.append((nr, nc, dr, dc))

            if neighbors:
                # Выбираем случайное направление
                nr, nc, dr, dc = random.choice(neighbors)
                # Ломаем стенку между текущей и новой ячейкой
                self.grid[r + dr // 2][c + dc // 2] = 0
                self.grid[nr][nc] = 0
                stack.append((nr, nc))
            else:
                stack.pop()

    def move_player(self, dr, dc):
        """Перемещение игрока с проверкой коллизии со стенами"""
        if self.is_won:
            return

        new_r = self.player_r + dr
        new_c = self.player_c + dc

        if 0 <= new_r < GRID_ROWS and 0 <= new_c < GRID_COLS:
            if self.grid[new_r][new_c] == 0:
                self.player_r = new_r
                self.player_c = new_c

        if (self.player_r, self.player_c) == self.finish_pos:
            self.is_won = True


class Game:
    """Главный контроллер"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Игровой лабиринт")
        self.clock = pygame.time.Clock()

        self.backend = Backend()
        self.graphics = Graphics(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.backend.reset()
                    
                    # Пошаговое управление по нажатию клавиш
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        self.backend.move_player(-1, 0)
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.backend.move_player(1, 0)
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        self.backend.move_player(0, -1)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.backend.move_player(0, 1)

            self.graphics.draw_maze(
                self.backend.grid, 
                self.backend.start_pos, 
                self.backend.finish_pos
            )
            self.graphics.draw_player(
                self.backend.player_r, 
                self.backend.player_c
            )
            self.graphics.draw_ui(self.backend.is_won)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()