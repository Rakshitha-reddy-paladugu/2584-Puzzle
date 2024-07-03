import random
import pygame
from pygame.locals import *
from pygame import mixer

# Initialize mixer and play the initial sound
mixer.init()
mixer.music.load(r"C:\Users\HP\OneDrive\Desktop\2584 game\button-pressed-38129.mp3")
mixer.music.play()

# Initialize pygame
pygame.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('2584')

# Load fonts
font = pygame.font.SysFont('oswald', 50)
font1 = pygame.font.SysFont('Architects Daughter', 50)
font2 = pygame.font.SysFont('oswald', 33)
font3 = pygame.font.SysFont('oswald', 50)

# Render texts
score_text = font.render('SCORE:', True, (0, 0, 0))
start_text = font3.render("Start the Game", True, (0, 0, 0))
quit_text = font3.render("Quit the Game", True, (0, 0, 0))

# Load images
background_img = pygame.image.load('img.jpg')
programIcon = pygame.image.load('logo.JPEG')
gameover_img = pygame.image.load('gameover.png')
start_pic_img = pygame.image.load('start.jpg')
pygame.display.set_icon(programIcon)

# Constants and initializations
lst_score = []
lst = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]

def position_grid(grid):
    lst1 = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                lst1.append([i, j])
    return lst1

def generate_1(grid, k=2):
    for _ in range(k):
        if not position_grid(grid):
            return grid
        pos = random.choice(position_grid(grid))
        grid[pos[0]][pos[1]] = 1
    return grid

def reverse(grid):
    return [row[::-1] for row in grid]

def transp(grid):
    return [list(row) for row in zip(*grid)]

def compress(grid):
    new_grid = [[0]*4 for _ in range(4)]
    for i in range(4):
        pos_new = 0
        for j in range(4):
            if grid[i][j] != 0:
                new_grid[i][pos_new] = grid[i][j]
                pos_new += 1
    return new_grid

def merge(grid):
    for i in range(4):
        for j in range(3):
            if grid[i][j] == 1 and grid[i][j + 1] == 1:
                mixer.music.load(r"C:\Users\HP\OneDrive\Desktop\2584 game\button-pressed-38129.mp3")
                mixer.music.play()
                grid[i][j] += grid[i][j + 1]
                lst_score.append(grid[i][j])
                grid[i][j + 1] = 0
            elif grid[i][j] in lst and (grid[i][j + 1] == lst[lst.index(grid[i][j]) + 1] or grid[i][j + 1] == lst[lst.index(grid[i][j]) - 1]):
                mixer.music.load(r"C:\Users\HP\OneDrive\Desktop\2584 game\button-pressed-38129.mp3")
                mixer.music.play()
                grid[i][j] += grid[i][j + 1]
                grid[i][j + 1] = 0
                lst_score.append(grid[i][j])
    return grid

def moveLeft(grid):
    return generate_1(compress(merge(compress(grid))), k=1)

def moveRight(grid):
    return generate_1(reverse(compress(merge(compress(reverse(grid))))), k=1)

def moveUp(grid):
    return generate_1(transp(compress(merge(compress(transp(grid))))), k=1)

def moveDown(grid):
    return generate_1(transp(reverse(compress(merge(compress(reverse(transp(grid))))))), k=1)

def game_status(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 2584:
                return 'WON'
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                return 'GAME NOT OVER'
    for i in range(4):
        for j in range(3):
            if grid[i][j] == 1 and grid[i][j + 1] == 1:
                return 'GAME NOT OVER'
    for i in range(3):
        for j in range(4):
            if grid[i][j] == 1 and grid[i + 1][j] == 1:
                return 'GAME NOT OVER'
    for i in range(4):
        for j in range(3):
            if (grid[i][j] in lst and (grid[i][j + 1] == lst[lst.index(grid[i][j]) + 1] or grid[i][j + 1] == lst[lst.index(grid[i][j]) - 1])):
                return 'GAME NOT OVER'
    for i in range(3):
        for j in range(4):
            if (grid[i][j] in lst and (grid[i + 1][j] == lst[lst.index(grid[i][j]) + 1] or grid[i + 1][j] == lst[lst.index(grid[i][j]) - 1])):
                return 'GAME NOT OVER'
    return 'LOST'

def restart():
    lst_score.clear()
    return generate_1([[0]*4 for _ in range(4)], k=2)

def rectangle(grid):
    cell_size = min(screen_width, screen_height) // 5  # Size of each cell to fit 4x4 grid with gaps
    margin_x = (screen_width - cell_size * 4) // 2
    margin_y = (screen_height - cell_size * 4) // 2
    gap_size = cell_size // 10  # Size of the gap between cells

    screen.fill((255, 255, 255))
    screen.blit(pygame.transform.scale(background_img, (screen_width, screen_height)), (0, 0))

    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(
                margin_x + j * (cell_size + gap_size), 
                margin_y + i * (cell_size + gap_size), 
                cell_size, cell_size), border_radius=8)
            text_surface = font.render(f'{grid[i][j]}', True, (0, 0, 0) if grid[i][j] else (200, 200, 200))
            text_rectangle = text_surface.get_rect(center=(
                margin_x + j * (cell_size + gap_size) + cell_size // 2, 
                margin_y + i * (cell_size + gap_size) + cell_size // 2))
            screen.blit(text_surface, text_rectangle)

    score_surface = font.render(f'{sum(lst_score)}', True, (0, 0, 0))
    score_txt = score_surface.get_rect(center=(200, 635))
    screen.blit(score_surface, score_txt)
    screen.blit(score_text, (20, 620))

    # Draw Restart and End buttons
    button_restart = pygame.Rect(margin_x - cell_size - gap_size * 3, margin_y, cell_size, cell_size // 2)
    button_end = pygame.Rect(margin_x - cell_size - gap_size * 3, margin_y + cell_size, cell_size, cell_size // 2)
    draw_button(button_restart, "Restart")
    draw_button(button_end, "End")

    pygame.display.flip()
    return button_restart, button_end

def keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'q'
        if event.type == KEYDOWN:
            if event.key == K_TAB:
                return 't'
            elif event.key == K_ESCAPE:
                return 'q'
            elif event.key == K_LEFT:
                return 'l'
            elif event.key == K_RIGHT:
                return 'r'
            elif event.key == K_DOWN:
                return 'd'
            elif event.key == K_UP:
                return 'u'
            elif event.key == K_SPACE:
                return 'space'
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                return event.pos

def draw_button(rect, text):
    pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=8)  # Black border
    inner_rect = rect.inflate(-6, -6)  # Slightly smaller inner rectangle
    pygame.draw.rect(screen, (135, 206, 250), inner_rect, border_radius=8)  # Sky blue fill
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=inner_rect.center)
    screen.blit(text_surface, text_rect)

def start():
    running = True
    while running:
        screen.blit(pygame.transform.scale(start_pic_img, (screen_width, screen_height)), (0, 0))

        button1 = pygame.Rect((screen_width // 2 - 200, screen_height // 2 - 30), (400, 50))
        button2 = pygame.Rect((screen_width // 2 - 200, screen_height // 2 + 50), (400, 50))

        draw_button(button1, "Start the Game")
        draw_button(button2, "Quit the Game")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if button1.collidepoint(event.pos):
                        game_loop()
                    elif button2.collidepoint(event.pos):
                        pygame.quit()

def game_loop(grid=None):
    if grid is None:
        grid = restart()
    while True:
        action = keys()
        if action == 'q':
            pygame.quit()
        elif action == 't':
            start()
        elif action == 'l':
            grid = moveLeft(grid)
        elif action == 'r':
            grid = moveRight(grid)
        elif action == 'd':
            grid = moveDown(grid)
        elif action == 'u':
            grid = moveUp(grid)
        elif action == 'space':
            grid = restart()
        elif isinstance(action, tuple):  # If the action is a mouse click position
            button_restart, button_end = rectangle(grid)
            if button_restart.collidepoint(action):
                grid = restart()
            elif button_end.collidepoint(action):
                pygame.quit()

        rectangle(grid)
        if game_status(grid) == 'WON':
            screen.blit(gameover_img, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            return 'WON'
        elif game_status(grid) == 'LOST':
            screen.blit(gameover_img, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            return 'LOST'

if __name__ == "__main__":
    start()
