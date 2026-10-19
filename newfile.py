import pygame
import random

# Initialize Pygame
pygame.init()

# Display Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 25

# Grid Dimensions (Standard LCD Brick Game Style: 10x20)
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
BLACK = (15, 20, 15)       # LCD Dark / Off-black
LCD_BG = (160, 180, 140)   # Classic LCD Greenish Grey Background
PIXEL_COLOR = (20, 30, 20) # Active LCD Pixels

SHAPES = [
    [[1, 1, 1, 1]],          # I
    [[1, 1], [1, 1]],        # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

class LCDFallingBlocks:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("LCD Falling Blocks - Patriot Edition")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 0
        self.game_over = False
        
        self.next_shape = random.choice(SHAPES)
        self.spawn_piece()

    def spawn_piece(self):
        self.current_shape = self.next_shape
        self.next_shape = random.choice(SHAPES)
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

        if self.check_collision(0, 0, self.current_shape):
            self.game_over = True

    def check_collision(self, offset_x, offset_y, shape):
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + c + offset_x
                    new_y = self.current_y + r + offset_y
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def merge_piece(self):
        for r, row in enumerate(self.current_shape):
            for c, cell in enumerate(row):
                if cell and self.current_y + r >= 0:
                    self.grid[self.current_y + r][self.current_x + c] = 1
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        lines_cleared = 0
        for r in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[r]):
                del self.grid[r]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1

        if lines_cleared > 0:
            self.score += lines_cleared * 100
            self.level = self.score // 500

    def rotate_shape(self):
        rotated = [list(row) for row in zip(*self.current_shape[::-1])]
        if not self.check_collision(0, 0, rotated):
            self.current_shape = rotated

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def run(self):
        fall_time = 0
        
        while not self.game_over:
            fall_speed = max(100, 500 - (self.level * 40)) # Speeds up as level increases
            delta_time = self.clock.tick(60)
            fall_time += delta_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(-1, 0, self.current_shape):
                        self.current_x -= 1
                    elif event.key == pygame.K_RIGHT and not self.check_collision(1, 0, self.current_shape):
                        self.current_x += 1
                    elif event.key == pygame.K_DOWN and not self.check_collision(0, 1, self.current_shape):
                        self.current_y += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()

            if fall_time >= fall_speed:
                if not self.check_collision(0, 1, self.current_shape):
                    self.current_y += 1
                else:
                    self.merge_piece()
                fall_time = 0

            # Render Screen
            self.screen.fill(LCD_BG)

            # Draw Main Grid
            grid_origin_x = 20
            grid_origin_y = 50
            for r in range(GRID_HEIGHT):
                for c in range(GRID_WIDTH):
                    cell_x = grid_origin_x + c * BLOCK_SIZE
                    cell_y = grid_origin_y + r * BLOCK_SIZE
                    color = PIXEL_COLOR if self.grid[r][c] else (140, 160, 120)
                    self.draw_cell(cell_x, cell_y, color)

            # Draw Current Falling Piece
            for r, row in enumerate(self.current_shape):
                for c, cell in enumerate(row):
                    if cell:
                        cell_x = grid_origin_x + (self.current_x + c) * BLOCK_SIZE
                        cell_y = grid_origin_y + (self.current_y + r) * BLOCK_SIZE
                        self.draw_cell(cell_x, cell_y, PIXEL_COLOR)

            # Draw HUD (Score & Speed Level)
            font = pygame.font.SysFont("monospace", 18, bold=True)
            score_text = font.render(f"SCORE: {self.score:05d}", True, PIXEL_COLOR)
            level_text = font.render(f"SPEED: {self.level:02d}", True, PIXEL_COLOR)
            self.screen.blit(score_text, (280, 50))
            self.screen.blit(level_text, (280, 100))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = LCDFallingBlocks()
    game.run()
