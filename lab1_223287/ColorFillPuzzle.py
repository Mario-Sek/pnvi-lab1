import random
import pygame

WIDTH = 700
HEIGHT = 750
GRID_SIZE = 5
SQUARE_SIZE = 70
GRID_WIDTH = SQUARE_SIZE * GRID_SIZE
GRID_HEIGHT = SQUARE_SIZE * GRID_SIZE
GRID_X_OFFSET = (WIDTH - GRID_WIDTH) // 2
GRID_Y_OFFSET = (HEIGHT - GRID_HEIGHT - 120) // 2

COLORS = [
    (255, 99, 71),
    (50, 205, 50),
    (34, 193, 195),
    (255, 165, 0)
]

pygame.init()
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 40)

grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
previous_states = []
selected_color = COLORS[0]
game_over = False

def draw_text(text, font, color, x, y, center=True):
    text_surf = font.render(text, True, color)
    if center:
        x -= text_surf.get_width() // 2
    screen.blit(text_surf, (x, y-9))

def draw_button(x, y, width, height, text):
    button = pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 3)
    draw_text(text, font, (0, 0, 0), x + width // 2, y + height // 2, center=True)
    return button

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col] or (255, 255, 255)
            rect = (GRID_X_OFFSET + col * SQUARE_SIZE, GRID_Y_OFFSET + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

def is_valid_move(row, col, color):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return all(
        not (0 <= row + dr < GRID_SIZE and 0 <= col + dc < GRID_SIZE and grid[row + dr][col + dc] == color)
        for dr, dc in directions
    )

def is_solved():
    return all(cell is not None for row in grid for cell in row)

def reset_game():
    global grid, selected_color, game_over, previous_states
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    selected_color, game_over = COLORS[0], False
    previous_states.clear()
    fill_random_squares()

def undo_move():
    global grid
    if previous_states:
        grid = previous_states.pop()

def fill_random_squares():
    for _ in range(5):
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        color = random.choice(COLORS)
        grid[row][col] = color

def game_loop():
    global selected_color, game_over

    running = True
    color_cycle_index = 0
    last_color_change_time = pygame.time.get_ticks()

    fill_random_squares()

    while running:
        screen.fill((211, 211, 211))
        if game_over:
            if pygame.time.get_ticks() - last_color_change_time >= 1000:
                last_color_change_time = pygame.time.get_ticks()
                color_cycle_index = (color_cycle_index + 1) % len(COLORS)
            screen.fill(COLORS[color_cycle_index])
            draw_text("Well done!", title_font, (0, 0, 0), WIDTH // 2, 45)
        else:
            draw_text("Color Filling Puzzle", title_font, (0, 0, 0), WIDTH // 2, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if reset_button.collidepoint(mx, my):
                    reset_game()
                elif not game_over and undo_button.collidepoint(mx, my):
                    undo_move()
                elif not game_over:
                    col, row = (mx - GRID_X_OFFSET) // SQUARE_SIZE, (my - GRID_Y_OFFSET) // SQUARE_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] is None:
                        if is_valid_move(row, col, selected_color):
                            previous_states.append([r[:] for r in grid])
                            grid[row][col] = selected_color

        if is_solved():
            game_over = True

        draw_grid()

        button_radius = 25
        padding = 10
        color_palette_y = HEIGHT - 124
        button_x_offset = (WIDTH - 4 * (button_radius * 2 + padding)) // 2
        for i, color in enumerate(COLORS):
            cx = button_x_offset + i * (button_radius * 2 + padding) + button_radius
            cy = color_palette_y + button_radius

            if color == selected_color:
                pygame.draw.circle(screen, (0, 0, 0), (cx, cy), button_radius + 4)
                pygame.draw.circle(screen, (255, 255, 255), (cx, cy), button_radius + 2)

            pygame.draw.circle(screen, color, (cx, cy), button_radius)

            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if ((mx - cx) ** 2 + (my - cy) ** 2) ** 0.5 <= button_radius:
                    selected_color = color

        draw_text("colors:", font, (0, 0, 0), WIDTH // 2, HEIGHT - 150)

        button_y = HEIGHT - 200
        undo_button = draw_button(WIDTH // 2 - 70, button_y, 60, 30, "Undo")
        reset_button = draw_button(WIDTH // 2 + 10, button_y, 60, 30, "Reset")

        pygame.display.update()

game_loop()
pygame.quit()
