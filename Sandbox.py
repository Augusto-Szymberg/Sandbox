import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions for multi-panel
center_panel_width = 800
center_panel_height = 800
side_panel_width = 150
screen_width = center_panel_width + 2 * side_panel_width
screen_height = center_panel_height

# New variables for brush size and burst size radius
brush_size = 2  # The radius of the brush in grid cells
burst_size_radius = 2  # The radius of the burst size

# Particle IDs
PARTICLE_IDS = {"Empty": 0, "Sand": 1, "Water": 2, "Dirt": 3, "Stone": 4, "Brick": 5, "Acid": 6, "Oil": 7, "Fire": 8, "Lava": 9, "BurningOil": 10, "Smoke": 11}

# Colors
WHITE = (255, 255, 255); RED = (255, 0, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255)
LIGHT_GREY = (211, 211, 211); DARK_GREY = (169, 169, 169)

# Set up the display for multi-panel
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Multi-Panel Screen with Particle Simulator')

# Particle simulator constants
GRID_SIZE = 10
ROWS = center_panel_height // GRID_SIZE
COLS = center_panel_width // GRID_SIZE
BG_COLOR = (173, 216, 230)

class Particle:
    def __init__(self, particle_type):
        self.type = particle_type

    def update(self, grid, x, y):
        pass

    def isLiquid(self):
        return False

class Liquid(Particle):
    def __init__(self, particle_type, density):
        super().__init__(particle_type)
        self.density = density

    def update(self, grid, x, y):
        # Liquid specific update logic, including density check
        if y < ROWS - 1:
            below = grid[x][y + 1]
            if isinstance(below, Liquid) and self.density < below.density:
                grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
            elif below == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            else:
                move_horizontally = random.choice([-1, 1])
                new_x = x + move_horizontally
                if 0 <= new_x < COLS and grid[new_x][y] == PARTICLE_IDS["Empty"]:
                    grid[new_x][y], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
    
    def isLiquid(self):
        return True

class Sand(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Sand"])
        self.color = random.choice([(194, 178, 128), (189, 174, 123), (199, 183, 133), (204, 188, 138)])

    def update(self, grid, x, y):
        if y < ROWS - 1:
            # Check directly below -Gravity-
            if grid[x][y + 1] == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            # Exchange places with liquids
            elif isinstance(grid[x][y + 1], Particle) and (is_position_liquid(grid, x, (y + 1)) or is_position_liquid(grid, (x + 1), (y + 1)) or is_position_liquid(grid, (x - 1), (y + 1))):
                if is_position_liquid(grid, x, (y + 1)): # Down
                    grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
                elif is_position_liquid(grid, (x + 1), (y + 1)): # Right-Diagonal
                    grid[x + 1][y + 1], grid[x][y] = grid[x][y], grid[x + 1][y + 1]
                elif is_position_liquid(grid, (x - 1), (y + 1)): # Left-Diagonal
                    grid[x - 1][y + 1], grid[x][y] = grid[x][y], grid[x - 1][y + 1]
            # Check diagonally below
            else:
                for dx in [-1, 1]:
                    if 0 <= x + dx < COLS and grid[x + dx][y + 1] == PARTICLE_IDS["Empty"]:
                        grid[x + dx][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
                        break

class Water(Liquid):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Water"], density=1)
        self.color = (64, 164, 223)

    def update(self, grid, x, y):
        super().update(grid, x, y)

class Dirt(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Dirt"])
        self.color = random.choice([(128, 89, 25), (133, 93, 26), (122, 92, 41), (133, 94, 28)])

    def update(self, grid, x, y):
        if y < ROWS - 1:
            # Check directly below -Gravity-
            if grid[x][y + 1] == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            # Liquids Below
            elif isinstance(grid[x][y + 1], Particle) and is_position_liquid(grid, x, (y + 1)):
                if is_position_liquid(grid, x, (y + 1)): # Down
                    grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
            # Diagonals (Less Granularity)
            elif y < ROWS - 3:
                if isinstance(grid[x][y + 1], Dirt) and isinstance(grid[x][y + 2], Dirt) and isinstance(grid[x][y + 3], Dirt):
                    # Liquid Diagonals
                    if is_position_liquid(grid, (x + 1), (y + 3)): # 3D-1R 
                        grid[x + 1][y + 3], grid[x][y] = grid[x][y], grid[x + 1][y + 3]
                    elif is_position_liquid(grid, (x - 1), (y + 3)): # 3D-1L 
                        grid[x - 1][y + 3], grid[x][y] = grid[x][y], grid[x - 1][y + 3]
                    # Empty Diagonals
                    elif is_position_empty(grid, (x + 1), (y + 3)): # 3D-1R
                        grid[x + 1][y + 3], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
                    elif is_position_empty(grid, (x - 1), (y + 3)): # 3D-1L 
                        grid[x - 1][y + 3], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]

class Stone(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Stone"])
        self.color = random.choice([(136, 140, 141), (130, 134, 135), (124, 133, 135), (117, 121, 122)])
        self.lava_transformation_delay = 10  # Delay for lava transformation
        self.delay_counter = 0
    
    def update(self, grid, x, y):
        if y < ROWS - 1:
            # Check directly below -Gravity-
            if grid[x][y + 1] == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            # Liquids -Gravity-
            elif isinstance(grid[x][y + 1], Particle) and is_position_liquid(grid, x, (y + 1)):
                if is_position_liquid(grid, x, (y + 1)): # Down
                    grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                if isinstance(grid[new_x][new_y], Lava):
                    self.delay_counter += 1
                    if self.delay_counter >= self.lava_transformation_delay:
                        grid[x][y] = create_particle(PARTICLE_IDS["Lava"])
                    return  # Return here to stop checking further
        self.delay_counter = 0  # Reset counter if no lava is adjacent

class Brick(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Brick"])
        self.color = (121, 59, 49)
    
    def update(self, grid, x, y):
        pass

class Acid(Liquid):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Acid"], density=0.5)
        self.color = (176, 191, 26)
        self.dissolve_counter = 0  # Counter for dissolving blocks
        self.dissolve_threshold = 5  # Number of frames to dissolve a block

    def update(self, grid, x, y):
        reacted = False  # Flag to check if acid has reacted

        # Check all adjacent cells (above, below, left, right)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = x + dx, y + dy

            # Check if coordinates are within grid bounds
            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                adjacent = grid[new_x][new_y]

                # If adjacent is not a brick, not empty, and not another liquid
                if adjacent != PARTICLE_IDS["Brick"] and adjacent != PARTICLE_IDS["Empty"] and not isinstance(adjacent, Liquid):
                    # Increment the counter
                    self.dissolve_counter += 1
                    reacted = True

                    # Check if the dissolve counter has reached the threshold
                    if self.dissolve_counter >= self.dissolve_threshold:
                        # Destroy the adjacent particle
                        grid[new_x][new_y] = PARTICLE_IDS["Empty"]
                        # Reset the counter
                        self.dissolve_counter = 0
                        # Destroy itself
                        grid[x][y] = PARTICLE_IDS["Empty"]
                        return
                    break  # Stop checking further if reacted

        if not reacted:
            # If no reaction, reset the counter and behave like a normal liquid
            self.dissolve_counter = 0
            super().update(grid, x, y)

class Oil(Liquid):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Oil"], density=0.8)
        self.color = (50, 61, 46)

    def update(self, grid, x, y):
        # Check adjacent cells for fire, burning oil or lava
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                adjacent = grid[new_x][new_y]
                if isinstance(adjacent, Fire) or isinstance(adjacent, BurningOil) or isinstance(adjacent, Lava):
                    grid[x][y] = create_particle(PARTICLE_IDS["BurningOil"])
                    return  # Transform into burning oil and stop checking further
        super().update(grid, x, y)

class BurningOil(Liquid):
    def __init__(self):
        super().__init__(PARTICLE_IDS["BurningOil"], density=0.8)
        # More subtle color changes
        self.colors = [(255, 100, 0), (255, 110, 10), (255, 120, 20), (255, 130, 30)] 
        self.color = random.choice(self.colors)
        self.color_change_delay = random.randint(6, 8)
        self.delay_counter = 0
        self.lifetime = 200  # Lifespan of burning oil
        self.age = 0

    def update(self, grid, x, y):
        self.age += 1
        self.delay_counter += 1

        # Color change logic
        if self.delay_counter >= self.color_change_delay:
            self.color = random.choice(self.colors)
            self.delay_counter = 0

        # Chance to create fire above
        if random.random() < 0.05 and y > 0:  # 10% chance to create fire
            if grid[x][y - 1] == PARTICLE_IDS["Empty"]:
                grid[x][y - 1] = create_particle(PARTICLE_IDS["Fire"])

        # Lifespan check
        if self.age >= self.lifetime:
            grid[x][y] = create_particle(PARTICLE_IDS["Smoke"])

        super().update(grid, x, y)

class Fire(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Fire"])
        self.colors = [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 165, 0)]  # Different shades of fire
        self.color = random.choice(self.colors)
        self.move_delay = random.randint(8, 10)  # Frames between upward movements
        self.total_lifetime = random.randint(46, 92)  # Total lifetime before turning into smoke
        self.age = 0  # Current age of the fire particle
        self.delay_counter = 0  # Counter for movement delay

    def update(self, grid, x, y):
        self.age += 1
        self.delay_counter += 1

        if self.age >= self.total_lifetime:
            # Turn into smoke
            grid[x][y] = create_particle(PARTICLE_IDS["Smoke"])
        elif self.delay_counter >= self.move_delay:
            self.delay_counter = 0  # Reset delay counter
            self.color = random.choice(self.colors)  # Change Color

            # Random chance to move sideways
            if random.random() < 0.3:  # 30% chance to move sideways
                dx = random.choice([-1, 1])
                new_x = x + dx
                if 0 <= new_x < COLS and y > 0 and grid[new_x][y - 1] == PARTICLE_IDS["Empty"]:
                    grid[new_x][y - 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            # Move upwards
            elif y > 0 and grid[x][y - 1] == PARTICLE_IDS["Empty"]:
                grid[x][y - 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]

class Smoke(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Smoke"])
        self.colors = [(128, 128, 128), (135, 135, 135), (142, 142, 142), (149, 149, 149)]  # Different shades of gray for smoke
        self.color = random.choice(self.colors)
        self.move_delay = random.randint(8, 10)  # Frames between upward movements
        self.delay_counter = 0  # Counter for movement delay

    def update(self, grid, x, y):
        self.delay_counter += 1
        if self.delay_counter >= self.move_delay:
            self.delay_counter = 0  # Reset delay counter
            self.color = random.choice(self.colors)  # Change color

            # Eliminate smoke at the top
            if y == 0:
                # Smoke disappears at the top
                grid[x][y] = PARTICLE_IDS["Empty"]
            # Random chance to move sideways
            elif random.random() < 0.3:  # 30% chance to move sideways
                dx = random.choice([-1, 1])
                new_x = x + dx
                if 0 <= new_x < COLS and y > 0 and grid[new_x][y - 1] == PARTICLE_IDS["Empty"]:
                    grid[new_x][y - 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            # Move upwards
            elif y > 0 and grid[x][y - 1] == PARTICLE_IDS["Empty"]:
                grid[x][y - 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]

class Lava(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Lava"])
        self.colors = [(207, 16, 32), (217, 30, 24), (227, 45, 34), (237, 55, 43)]  # Subtle shades of red and orange
        self.color = random.choice(self.colors)
        self.color_change_delay = random.randint(10, 15)  # Frames between color changes
        self.delay_counter = 0

    def update(self, grid, x, y):
        # Check adjacent cells for water
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                if isinstance(grid[new_x][new_y], Water):
                    grid[x][y] = create_particle(PARTICLE_IDS["Stone"])  # Transform lava into stone
                    grid[new_x][new_y] = create_particle(PARTICLE_IDS["Smoke"])  # Transform water into smoke
                    return  # Stop further checks after transformation

        # Lava specific update logic
        if y < ROWS - 1:
            below = grid[x][y + 1]
            if below == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            else:
                move_horizontally = random.choice([-1, 1])
                new_x = x + move_horizontally
                if 0 <= new_x < COLS and grid[new_x][y] == PARTICLE_IDS["Empty"]:
                    grid[new_x][y], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
        # Occasionally create fire on top
        if random.random() < 0.002 and y > 0:  # 1% chance to create fire
            if grid[x][y - 1] == PARTICLE_IDS["Empty"]:
                grid[x][y - 1] = create_particle(PARTICLE_IDS["Fire"])
        self.delay_counter += 1
        if self.delay_counter >= self.color_change_delay:
            self.color = random.choice(self.colors)  # Change color
            self.delay_counter = 0  # Reset delay counter

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        # Draw the button rectangle
        pygame.draw.rect(surface, LIGHT_GREY, self.rect)
        # Draw the button text
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
            
def create_particle(particle_type_id):
    if particle_type_id == PARTICLE_IDS["Sand"]:
        return Sand()
    elif particle_type_id == PARTICLE_IDS["Water"]:
        return Water()
    elif particle_type_id == PARTICLE_IDS["Dirt"]:
        return Dirt()
    elif particle_type_id == PARTICLE_IDS["Stone"]:
        return Stone()
    elif particle_type_id == PARTICLE_IDS["Brick"]:
        return Brick()
    elif particle_type_id == PARTICLE_IDS["Acid"]:
        return Acid()
    elif particle_type_id == PARTICLE_IDS["Oil"]:
        return Oil()
    elif particle_type_id == PARTICLE_IDS["Fire"]:
        return Fire()
    elif particle_type_id == PARTICLE_IDS["BurningOil"]:
        return BurningOil()
    elif particle_type_id == PARTICLE_IDS["Smoke"]:
        return Smoke()
    elif particle_type_id == PARTICLE_IDS["Lava"]:
        return Lava()
    return None  # For Empty and other cases

def update_particles(grid):
    # Iterate backwards through the grid to handle particles moving down or sideways
    for y in range(ROWS - 2, -1, -1):
        for x in range(COLS):
            particle = grid[x][y]
            if isinstance(particle, Particle):
                particle.update(grid, x, y)

    # Handle particles at the bottom row separately as they only move sideways
    for x in range(COLS):
        particle = grid[x][ROWS - 1]
        if isinstance(particle, Particle):
            particle.update(grid, x, ROWS - 1)

def draw_grid(offset_x):
    for x in range(0, center_panel_width, GRID_SIZE):
        for y in range(0, center_panel_height, GRID_SIZE):
            rect = pygame.Rect(x + offset_x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BG_COLOR, rect)

def draw_particles(grid, offset_x):
    for x in range(COLS):
        for y in range(ROWS):
            if isinstance(grid[x][y], Particle):
                rect = pygame.Rect(x * GRID_SIZE + offset_x, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, grid[x][y].color, rect)

def draw_selection(current_selection, offset_x, font):
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

    text = font.render(selection_text, True, (255, 255, 255))
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

def change_brush_size(new_size, new_burst_size):
    global brush_size
    global burst_size_radius
    brush_size = new_size
    burst_size_radius = new_burst_size

def main():
    global brush_size
    grid = [[0 for _ in range(ROWS)] for _ in range(COLS)]
    current_selection = 1  # Modify as per your particle selection logic
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

    running = True
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
        # Update particles, draw grid, particles, and selection inside the central panel
        offset_x = side_panel_width  # Offset for the central panel
        update_particles(grid)  # Assuming this function updates the grid
        draw_grid(offset_x)
        draw_particles(grid, offset_x)
        draw_selection(current_selection, offset_x, font)

        # Calculate the adjusted mouse position on the grid
        grid_mouse_x = (mouse_x - offset_x) // GRID_SIZE
        grid_mouse_y = mouse_y // GRID_SIZE

        # Draw brush indicator as a grid-aligned square
        for dx in range(-brush_size, brush_size + 1):
            for dy in range(-brush_size, brush_size + 1):
                if dx**2 + dy**2 <= burst_size_radius**2:
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
        clock.tick(60)  # You can adjust the FPS as needed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
