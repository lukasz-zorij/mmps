import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, WHITE, (j*GRID_SIZE, i*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1), 1)
            if grid[i][j] != 0:
                pygame.draw.rect(screen, COLORS[grid[i][j]-1], (j*GRID_SIZE, i*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))

def new_piece():
    shape = random.choice(SHAPES)
    return {
        'shape': shape,
        'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0,
        'color': COLORS[SHAPES.index(shape)]
    }

def valid_move(grid, piece, x, y):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][i])):
            if piece['shape'][i][j]:
                if (x + j < 0 or x + j >= GRID_WIDTH or
                    y + i >= GRID_HEIGHT or
                    (y + i >= 0 and grid[y + i][x + j])):
                    return False
    return True

def add_to_grid(grid, piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][i])):
            if piece['shape'][i][j]:
                grid[piece['y'] + i][piece['x'] + j] = COLORS.index(piece['color']) + 1

def clear_lines(grid):
    lines_cleared = 0
    for i in range(len(grid)-1, -1, -1):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    return lines_cleared

def rotate_piece(piece):
    return {
        'shape': list(zip(*piece['shape'][::-1])),
        'x': piece['x'],
        'y': piece['y'],
        'color': piece['color']
    }

def draw_piece(piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][i])):
            if piece['shape'][i][j]:
                pygame.draw.rect(screen, piece['color'],
                                 ((piece['x'] + j) * GRID_SIZE,
                                  (piece['y'] + i) * GRID_SIZE,
                                  GRID_SIZE - 1, GRID_SIZE - 1))

def game_over(grid):
    return any(grid[0])

def main():
    grid = create_grid()
    current_piece = new_piece()
    next_piece = new_piece()
    score = 0
    level = 1
    fall_time = 0
    fall_speed = 0.5
    game_over_flag = False

    while not game_over_flag:
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            if valid_move(grid, current_piece, current_piece['x'], current_piece['y'] + 1):
                current_piece['y'] += 1
            else:
                add_to_grid(grid, current_piece)
                lines_cleared = clear_lines(grid)
                score += lines_cleared * 100
                if lines_cleared > 0:
                    level = min(10, score // 1000 + 1)
                    fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
                current_piece = next_piece
                next_piece = new_piece()
                if not valid_move(grid, current_piece, current_piece['x'], current_piece['y']):
                    game_over_flag = True
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_flag = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if valid_move(grid, current_piece, current_piece['x'] - 1, current_piece['y']):
                        current_piece['x'] -= 1
                if event.key == pygame.K_RIGHT:
                    if valid_move(grid, current_piece, current_piece['x'] + 1, current_piece['y']):
                        current_piece['x'] += 1
                if event.key == pygame.K_DOWN:
                    if valid_move(grid, current_piece, current_piece['x'], current_piece['y'] + 1):
                        current_piece['y'] += 1
                if event.key == pygame.K_UP:
                    rotated_piece = rotate_piece(current_piece)
                    if valid_move(grid, rotated_piece, rotated_piece['x'], rotated_piece['y']):
                        current_piece = rotated_piece

        screen.fill(BLACK)
        draw_grid(grid)
        draw_piece(current_piece)

        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 50))
        screen.blit(level_text, (SCREEN_WIDTH - 200, 100))

        # Draw next piece
        next_piece_surface = pygame.Surface((100, 100))
        next_piece_surface.fill(BLACK)
        for i in range(len(next_piece['shape'])):
            for j in range(len(next_piece['shape'][i])):
                if next_piece['shape'][i][j]:
                    pygame.draw.rect(next_piece_surface, next_piece['color'],
                                     (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
        screen.blit(next_piece_surface, (SCREEN_WIDTH - 150, 200))

        pygame.display.flip()

    # Game over screen
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    pygame.display.flip()

    # Wait for user to close the window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()