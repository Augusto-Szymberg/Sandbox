import pygame
import sys
import random
from config import *
from particles import create_particle, Particle
from ui_components import Button, ParticleSelectionButton, ParticleSelectionIndicator
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
    max_current_selection = 20
    min_current_selection = 1
    running = True
    mouse_held_down_left = False
    mouse_held_down_right = False

    # Load particle images
    # Solid
    sand_image = pygame.image.load('imgs/sand.png')
    dirt_image = pygame.image.load('imgs/dirt.png')
    grass_image = pygame.image.load('imgs/grass.png')
    stone_image = pygame.image.load('imgs/stone.png')
    brick_image = pygame.image.load('imgs/brick.png')
    wood_image = pygame.image.load('imgs/wood.png')
    leaf_image = pygame.image.load('imgs/leaf.png')
    obsidian_image = pygame.image.load('imgs/obsidian.png')
    ice_image = pygame.image.load('imgs/ice.png')
    # Liquid
    water_image = pygame.image.load('imgs/water.png')
    acid_image = pygame.image.load('imgs/acid.png')
    oil_image = pygame.image.load('imgs/oil.png')
    lava_image = pygame.image.load('imgs/lava.png')
    liquid_nitrogen_image = pygame.image.load('imgs/liquidNitrogen.png')
    # Other
    fire_image = pygame.image.load('imgs/fire.png')
    methane_image = pygame.image.load('imgs/methane.png')
    grass_seed_image = pygame.image.load('imgs/seed.png')
    tree_seed_image = pygame.image.load('imgs/seed.png')
    # DEFAULT
    default_image = pygame.image.load('imgs/default.png')

    # Define buttons for changing brush size
    brush_size_buttons = [
        Button(10, 50, 130, 30, "Brush Size 1"),
        Button(10, 90, 130, 30, "Brush Size 2"),
        Button(10, 130, 130, 30, "Brush Size 3"),
        Button(10, 170, 130, 30, "Brush Size 4"),
        Button(10, 210, 130, 30, "Brush Size 5")
    ]

    # Create particle selection buttons in a grid
    # Particle categories
    solid_particles = ["Sand", "Dirt", "Grass", "Stone", "Brick", 
                       "Wood", "Leaf", "Obsidian", "Ice"]
    fluid_particles = ["Water", "Acid", "Oil", "Lava", "LiquidNitrogen"]
    other_particles = ["Fire", "Methane", "GrassSeed", "TreeSeed"]

    # Load particle images and IDs
    particle_images = {
        "Sand": sand_image, "Dirt": dirt_image, "Grass": grass_image, "Stone": stone_image, "Brick": brick_image,
        "Water": water_image, "Acid": acid_image, "Oil": oil_image, "Lava": lava_image, "Fire": fire_image, "Methane": methane_image, 
        "GrassSeed": grass_seed_image, "TreeSeed": tree_seed_image, "Wood": wood_image, "Leaf": leaf_image, 
        "LiquidNitrogen": liquid_nitrogen_image, "Obsidian": obsidian_image, "Ice": ice_image
    }

    # Particle Selection Indicator 
    id_to_name = {v: k for k, v in PARTICLE_IDS.items()} # Reverse Mapping
    particle_name = id_to_name[current_selection]
    particleSelectionIndicatorPadding = 25
    particleSelectionIndicatorWidth = 100
    particleSelectionIndicatorHeight = 100
    particleSelectionIndicator = ParticleSelectionIndicator(left_panel_width + center_panel_width + ((right_panel_width - particleSelectionIndicatorWidth)/2), particleSelectionIndicatorPadding, particleSelectionIndicatorWidth, particleSelectionIndicatorHeight, particle_images[particle_name], particle_name)

    # Function to create buttons for a category
    def create_buttons_for_category(category_particles, start_y):
        buttons = []
        for i, particle_name in enumerate(category_particles):
            row = i // grid_cols
            col = i % grid_cols
            x = start_x + (button_size + button_margin) * col
            y = start_y + (button_size + button_margin) * row
            button = ParticleSelectionButton(x, y, button_size, particle_images[particle_name], PARTICLE_IDS[particle_name])
            buttons.append(button)
        return buttons
    
    # Create particle selection buttons for each category
    solid_buttons = create_buttons_for_category(solid_particles, 220)
    fluid_buttons = create_buttons_for_category(fluid_particles, 430)  # Adjust Y start position as needed
    other_buttons = create_buttons_for_category(other_particles, 600)  # Adjust Y start position as needed
    particle_selection_buttons = solid_buttons + fluid_buttons + other_buttons

    # Font for category titles
    font = pygame.font.Font(None, 36)

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
                    # Buttons for Brush Size
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
                    # Buttons for Particle Selection
                    for button in particle_selection_buttons:
                        if button.is_clicked(event.pos):
                            current_selection = button.particle_id
                elif event.button == 3:  # Right click
                    mouse_held_down_right = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    mouse_held_down_left = False
                elif event.button == 3:  # Right click
                    mouse_held_down_right = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        offset_x = left_panel_width  # Offset for the central panel
        adjusted_mouse_x = mouse_x - offset_x

        if mouse_held_down_left or mouse_held_down_right:
            if 0 <= adjusted_mouse_x < center_panel_width:  # Check if within the central panel
                grid_x = adjusted_mouse_x // GRID_SIZE
                grid_y = mouse_y // GRID_SIZE

                # Calculate the affected area based on brush size
                for dx in range(-get_brush_size(), get_brush_size() + 1):
                    for dy in range(-get_brush_size(), get_brush_size() + 1):
                        if dx**2 + dy**2 <= get_burst_size()**2:
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

        # Update Particle Selection Indicator
        id_to_name = {v: k for k, v in PARTICLE_IDS.items()}  # Reverse Mapping

        if current_selection in id_to_name:
            particle_name = id_to_name[current_selection]
            particle_image = particle_images.get(particle_name, default_image)
        else:
            particle_name = "UNKNOWN"
            particle_image = default_image

        particleSelectionIndicator.set_image(particle_image)
        particleSelectionIndicator.set_text(particle_name)

        # Draw side panels
        pygame.draw.rect(screen, DARK_GREY, (0, 0, left_panel_width, screen_height))
        pygame.draw.rect(screen, DARK_GREY, (left_panel_width + center_panel_width, 0, right_panel_width, screen_height))

        # Draw brush size selection buttons
        for button in brush_size_buttons:
            button.draw(screen)

        # Draw particle indicator
        particleSelectionIndicator.draw(screen)
        # Draw separation line
        separationLineStartPos = (left_panel_width + center_panel_width, 165)
        separationLineEndPos = (left_panel_width + center_panel_width + right_panel_width, 165)
        pygame.draw.line(screen, LIGHT_GREY, separationLineStartPos, separationLineEndPos, 3)

        # Draw particle selection buttons and category titles
        for button in solid_buttons + fluid_buttons + other_buttons:
            button.draw(screen)
        # Render category titles
        solid_text = font.render("Solids", True, (0, 0, 0))
        fluid_text = font.render("Fluids", True, (0, 0, 0))
        other_text = font.render("Other", True, (0, 0, 0))
        screen.blit(solid_text, (left_panel_width + center_panel_height + 10, 190))  # Adjust positions as needed
        screen.blit(fluid_text, (left_panel_width + center_panel_height + 10, 400))  # Adjust positions as needed
        screen.blit(other_text, (left_panel_width + center_panel_height + 10, 570))  # Adjust positions as needed

        # Particle simulation logic
        offset_x = left_panel_width  # Offset for the central panel
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
