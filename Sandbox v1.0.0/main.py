import pygame
import sys
import random
from config import *
from particles import create_particle, Particle
from ui_components import Button
from utils import draw_grid, draw_particles, draw_selection, is_position_liquid, is_position_empty
from simulation import update_particles

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Multi-Panel Screen with Particle Simulator')

    grid = [[0 for _ in range(ROWS)] for _ in range(COLS)]
    current_selection = 1  
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    selectionCycle = [5]
    max_current_selection = 9
    min_current_selection = 1
    running = True
    mouse_held_down_left = False
    mouse_held_down_right = False

    # Define buttons for changing brush size
    brush_size_buttons = [
        Button(10, 50, 130, 30, "Brush Size 1"),
        Button(10, 90, 130, 30, "Brush Size 2"),
        Button(10, 130, 130, 30, "Brush Size 3"),
        Button(10, 170, 130, 30, "Brush Size 4"),
        Button(10, 210, 130, 30, "Brush Size 5")
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if current_selection > min_current_selection:
                        current_selection -= 1
                    else:
                        current_selection = max_current_selection
                elif event.key == pygame.K_RIGHT:
                    if current_selection < max_current_selection:
                        current_selection += 1
                    else:
                        current_selection = min_current_selection
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_held_down_left = True
                    for button in brush_size_buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "Brush Size 1":
                                change_brush_size(1, 0)
                            elif button.text == "Brush Size 2":
                                change_brush_size(1, 1)
                            elif button.text == "Brush Size 3":
                                change_brush_size(2, 2)
                            elif button.text == "Brush Size 4":
                                change_brush_size(3, 3)
                            elif button.text == "Brush Size 5":
                                change_brush_size(4, 4)
                elif event.button == 3:  # Right click
                    mouse_held_down_right = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    mouse_held_down_left = False
                elif event.button == 3:  # Right click
                    mouse_held_down_right = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset_x = side_panel_width  # Offset for the central panel
        adjusted_mouse_x = mouse_x - offset_x

        if mouse_held_down_left or mouse_held_down_right:
            if 0 <= adjusted_mouse_x < center_panel_width:  # Check if within the central panel
                grid_x = adjusted_mouse_x // GRID_SIZE
                grid_y = mouse_y // GRID_SIZE

                # Calculate the affected area based on brush size
                for dx in range(-brush_size, brush_size + 1):
                    for dy in range(-brush_size, brush_size + 1):
                        if dx**2 + dy**2 <= burst_size_radius**2:
                            new_x, new_y = grid_x + dx, grid_y + dy
                            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                                if mouse_held_down_left:
                                    # Check if the cell is empty before placing a new particle
                                    if grid[new_x][new_y] == PARTICLE_IDS["Empty"] and random.random() < 0.5:
                                        grid[new_x][new_y] = create_particle(current_selection)
                                elif mouse_held_down_right:
                                    grid[new_x][new_y] = PARTICLE_IDS["Empty"]

        # Clear the screen
        screen.fill(WHITE)

        # Draw side panels
        pygame.draw.rect(screen, DARK_GREY, (0, 0, side_panel_width, screen_height))
        pygame.draw.rect(screen, DARK_GREY, (side_panel_width + center_panel_width, 0, side_panel_width, screen_height))

        # Draw the buttons
        for button in brush_size_buttons:
            button.draw(screen)

        # Particle simulation logic
        offset_x = side_panel_width  # Offset for the central panel
        update_particles(grid)  # Assuming this function updates the grid
        draw_grid(screen, offset_x)
        draw_particles(screen, grid, offset_x)
        draw_selection(screen, current_selection, offset_x, font)

        # Calculate the adjusted mouse position on the grid
        grid_mouse_x = (mouse_x - offset_x) // GRID_SIZE
        grid_mouse_y = mouse_y // GRID_SIZE

        # Draw brush indicator as a grid-aligned square
        for dx in range(-get_brush_size(), get_brush_size() + 1):
            for dy in range(-get_brush_size(), get_brush_size() + 1):
                if dx**2 + dy**2 <= get_burst_size()**2:
                    square_x = grid_mouse_x + dx
                    square_y = grid_mouse_y + dy

                    # Check if the square is inside the center panel
                    if 0 <= square_x < COLS and 0 <= square_y < ROWS:
                        pixel_x = square_x * GRID_SIZE + offset_x
                        pixel_y = square_y * GRID_SIZE

                        # Create a separate surface for each square with semi-transparency
                        square_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        square_surface.fill((0, 0, 0, 128))  # Semi-transparent black
                        screen.blit(square_surface, (pixel_x, pixel_y))

        pygame.display.flip()
        clock.tick(60) # This controls the FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
