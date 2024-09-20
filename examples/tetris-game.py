import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_OFFSET_Y = SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE - 20

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

# Tetromino Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

# Set up game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[cell - 1],
                                 (GRID_OFFSET_X + x * BLOCK_SIZE,
                                  GRID_OFFSET_Y + y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE,
                             (GRID_OFFSET_X + x * BLOCK_SIZE,
                              GRID_OFFSET_Y + y * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE), 1)

def new_piece():
    shape = random.choice(SHAPES)
    return {
        'shape': shape,
        'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0,
        'color': COLORS[SHAPES.index(shape)]
    }

def valid_move(grid, piece, x_offset=0, y_offset=0):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece['x'] + x + x_offset
                new_y = piece['y'] + y + y_offset
                if (new_x < 0 or new_x >= GRID_WIDTH or
                    new_y >= GRID_HEIGHT or
                    (new_y >= 0 and grid[new_y][new_x])):
                    return False
    return True

def merge_piece(grid, piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                grid[piece['y'] + y][piece['x'] + x] = COLORS.index(piece['color']) + 1

def rotate_piece(piece):
    return {'shape': list(zip(*piece['shape'][::-1])),
            'x': piece['x'],
            'y': piece['y'],
            'color': piece['color']}

def clear_lines(grid):
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for line in full_lines:
        del grid[line]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(full_lines)

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, WHITE)
    rect = surface.get_rect()
    rect.midtop = (x, y)
    screen.blit(surface, rect)

def main():
    grid = create_grid()
    current_piece = new_piece()
    next_piece = new_piece()
    score = 0
    game_over = False

    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    level = 1

    while not game_over:
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time > 5000:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005
                level += 1

        if fall_time >= fall_speed * 1000:
            fall_time = 0
            if valid_move(grid, current_piece, y_offset=1):
                current_piece['y'] += 1
            else:
                merge_piece(grid, current_piece)
                lines_cleared = clear_lines(grid)
                score += lines_cleared * 100 * level
                current_piece = next_piece
                next_piece = new_piece()
                if not valid_move(grid, current_piece):
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid_move(grid, current_piece, x_offset=-1):
                    current_piece['x'] -= 1
                if event.key == pygame.K_RIGHT and valid_move(grid, current_piece, x_offset=1):
                    current_piece['x'] += 1
                if event.key == pygame.K_DOWN and valid_move(grid, current_piece, y_offset=1):
                    current_piece['y'] += 1
                if event.key == pygame.K_UP:
                    rotated = rotate_piece(current_piece)
                    if valid_move(grid, rotated):
                        current_piece = rotated
                if event.key == pygame.K_SPACE:
                    while valid_move(grid, current_piece, y_offset=1):
                        current_piece['y'] += 1
                    merge_piece(grid, current_piece)
                    lines_cleared = clear_lines(grid)
                    score += lines_cleared * 100 * level
                    current_piece = next_piece
                    next_piece = new_piece()
                    if not valid_move(grid, current_piece):
                        game_over = True

        screen.fill(BLACK)
        draw_grid(grid)
        
        for y, row in enumerate(current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece['color'],
                                     (GRID_OFFSET_X + (current_piece['x'] + x) * BLOCK_SIZE,
                                      GRID_OFFSET_Y + (current_piece['y'] + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(screen, WHITE, (GRID_OFFSET_X, GRID_OFFSET_Y,
                                         GRID_WIDTH * BLOCK_SIZE,
                                         GRID_HEIGHT * BLOCK_SIZE), 2)

        draw_text(f"Score: {score}", 30, SCREEN_WIDTH // 2, 10)
        draw_text(f"Level: {level}", 30, SCREEN_WIDTH // 2, 50)

        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 150, 100, 120, 120), 2)
        for y, row in enumerate(next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, next_piece['color'],
                                     (SCREEN_WIDTH - 140 + x * BLOCK_SIZE,
                                      110 + y * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()

    draw_text("GAME OVER", 60, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
    pygame.quit()