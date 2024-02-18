from config import GRID_SIZE, COLS, ROWS, PARTICLE_IDS, WHITE, DARK_GREY, side_panel_width, center_panel_width, center_panel_height, screen_height, brush_size, burst_size_radius, BG_COLOR
from particles import Particle
import pygame

def draw_grid(screen, offset_x):
    for x in range(0, center_panel_width, GRID_SIZE):
        for y in range(0, center_panel_height, GRID_SIZE):
            rect = pygame.Rect(x + offset_x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BG_COLOR, rect)

def draw_particles(screen, grid, offset_x):
    for x in range(COLS):
        for y in range(ROWS):
            if isinstance(grid[x][y], Particle):
                rect = pygame.Rect(x * GRID_SIZE + offset_x, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, grid[x][y].color, rect)

def draw_selection(screen, current_selection, offset_x, font):
    selection_text = "Current: "
    if current_selection == PARTICLE_IDS["Sand"]:
        selection_text += "Sand"
    elif current_selection == PARTICLE_IDS["Water"]:
        selection_text += "Water"
    elif current_selection == PARTICLE_IDS["Dirt"]:
        selection_text += "Dirt"
    elif current_selection == PARTICLE_IDS["Stone"]:
        selection_text += "Stone"
    elif current_selection == PARTICLE_IDS["Brick"]:
        selection_text += "Brick"
    elif current_selection == PARTICLE_IDS["Acid"]:
        selection_text += "Acid"
    elif current_selection == PARTICLE_IDS["Oil"]:
        selection_text += "Oil"
    elif current_selection == PARTICLE_IDS["Fire"]:
        selection_text += "Fire"
    elif current_selection == PARTICLE_IDS["Lava"]:
        selection_text += "Lava"
    else:
        selection_text += "Unknown"

    text= font.render(selection_text, True, (255, 255, 255))
    screen.blit(text, (offset_x + 10, 10))

def is_position_liquid(grid, x, y):
    if 0 <= x < COLS and 0 <= y < ROWS:
        particle = grid[x][y]
        if isinstance(particle, Particle):
            return particle.isLiquid()
    return False

def is_position_empty(grid, x, y):
    if 0 <= x < COLS and 0 <= y < ROWS:
        particle = grid[x][y]
        if particle == PARTICLE_IDS["Empty"]:
            return True
    return False
