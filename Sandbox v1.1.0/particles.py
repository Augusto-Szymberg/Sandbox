import random
from config import PARTICLE_IDS, ROWS, COLS

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
        self.color = random.choice([(121, 59, 49), (126, 64, 54), (116, 54, 44), (124, 56, 52)])
    
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
    return None

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