import random
from config import PARTICLE_IDS, ROWS, COLS

class Particle:
    def __init__(self, particle_type):
        self.type = particle_type

    def update(self, grid, x, y):
        pass

    def isLiquid(self):
        return False
    def isGas(self):
        return False

class Liquid(Particle):
    def __init__(self, particle_type, density):
        super().__init__(particle_type)
        self.density = density

    def update(self, grid, x, y):
        # Liquid specific update logic, including density check
        if y < ROWS - 1:
            below = grid[x][y + 1]
            if isinstance(below, Liquid) and self.density > below.density: # DOWN
                # Swap pos with lower density liquid
                grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
            # Gas Sorting
            elif isinstance(below, Gas):
                # Swap pos with gas particle
                grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
            # Normal Gravity
            elif below == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            else:
                # Check Left and Right for Density Sorting with Liquids
                move_horizontally = random.choice([-1, 1])
                if move_horizontally == -1: # LEFT
                    if x > 0:
                        left = grid[x - 1][y]
                        if isinstance(left, Liquid) and self.density > left.density:
                            grid[x - 1][y], grid[x][y] = grid[x][y], grid[x - 1][y]
                            return
                if move_horizontally == 1: # RIGHT
                    if x < COLS - 1:
                        right = grid[x + 1][y]
                        if isinstance(right, Liquid) and self.density > right.density:
                            grid[x + 1][y], grid[x][y] = grid[x][y], grid[x + 1][y]
                            return
                
                move_horizontally = random.choice([-1, 1])
                new_x = x + move_horizontally
                if 0 <= new_x < COLS and grid[new_x][y] == PARTICLE_IDS["Empty"]:
                    grid[new_x][y], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
    
    def isLiquid(self):
        return True
    def isGas(self):
        return False

class Gas(Particle):
    def __init__(self, particle_type):
        super().__init__(particle_type)

    def update(self, grid, x, y):
        # Gas always moves up if possible, but has a chance to move sideways
        move_sideways = random.choice([-1, 0, 1])  # Choose -1 (left), 0 (no horizontal move), or 1 (right)

        new_x = x + move_sideways
        new_y = y - 1  # Always move up

        # Check if new position is within grid bounds
        if 0 <= new_x < COLS and 0 <= new_y < ROWS:
            # Check if new position is empty
            if grid[new_x][new_y] == PARTICLE_IDS["Empty"]:
                # Move the gas particle
                grid[new_x][new_y], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
    
    def isLiquid(self):
        return False
    def isGas(self):
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

        # Check if the particle above, to the left, or to the right is empty
        is_empty_above = y > 0 and grid[x][y - 1] == PARTICLE_IDS["Empty"]
        is_empty_left = x > 0 and grid[x - 1][y] == PARTICLE_IDS["Empty"]
        is_empty_right = x < COLS - 1 and grid[x + 1][y] == PARTICLE_IDS["Empty"]

        if is_empty_above or is_empty_left or is_empty_right:
            # Check for grass in adjacent, diagonal, and extended diagonal cells
            for dx in [-1, 0, 1]:  # Check left, center, and right positions
                for dy in [-3, -2, -1, 1, 2, 3]:  # Check three up, two up, one up, one down, two down, three down
                    if 0 <= x + dx < COLS and 0 <= y + dy < ROWS:  # Ensure within grid bounds
                        # Skip checking the current position
                        if dx == 0 and dy == 0:
                            continue
                        if isinstance(grid[x + dx][y + dy], Grass):
                            # Random chance to convert to grass
                            if random.random() < 0.01:  # Adjust the probability as needed
                                grid[x][y] = Grass()
                            return  # Exit the method once conversion chance is checked

class Grass(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Grass"])
        self.color = random.choice([(75, 143, 65), (80, 147, 66), (69, 146, 81), (80, 148, 68)])

    def update(self, grid, x, y):
        has_moved = False

        if y < ROWS - 1:
            # Check directly below -Gravity-
            if grid[x][y + 1] == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
                has_moved = True
            # Liquids Below
            elif isinstance(grid[x][y + 1], Particle) and is_position_liquid(grid, x, (y + 1)):
                if is_position_liquid(grid, x, (y + 1)): # Down
                    grid[x][y + 1], grid[x][y] = grid[x][y], grid[x][y + 1]
                    has_moved = True
            # Fire
            elif isinstance(grid[x][y - 1], Fire): # DOWN
                grid[x][y] = create_particle(PARTICLE_IDS["Dirt"])
                return
            elif isinstance(grid[x + 1][y], Fire): # LEFT
                grid[x][y] = create_particle(PARTICLE_IDS["Dirt"])
                return
            elif isinstance(grid[x - 1][y], Fire): # RIGHT
                grid[x][y] = create_particle(PARTICLE_IDS["Dirt"])
                return
            # Diagonals (Less Granularity)
            elif y < ROWS - 3:
                if isinstance(grid[x][y + 1], Grass) and isinstance(grid[x][y + 2], Grass) and isinstance(grid[x][y + 3], Grass):
                    # Liquid Diagonals
                    if is_position_liquid(grid, (x + 1), (y + 3)): # 3D-1R 
                        grid[x + 1][y + 3], grid[x][y] = grid[x][y], grid[x + 1][y + 3]
                        has_moved = True
                    elif is_position_liquid(grid, (x - 1), (y + 3)): # 3D-1L 
                        grid[x - 1][y + 3], grid[x][y] = grid[x][y], grid[x - 1][y + 3]
                        has_moved = True
                    # Empty Diagonals
                    elif is_position_empty(grid, (x + 1), (y + 3)): # 3D-1R
                        grid[x + 1][y + 3], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
                        has_moved = True
                    elif is_position_empty(grid, (x - 1), (y + 3)): # 3D-1L 
                        grid[x - 1][y + 3], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
                        has_moved = True

        # Check if the particle to the right, left, or above is empty
        is_empty_above = y > 0 and grid[x][y - 1] == PARTICLE_IDS["Empty"]
        is_empty_left = x > 0 and grid[x - 1][y] == PARTICLE_IDS["Empty"]
        is_empty_right = x < COLS - 1 and grid[x + 1][y] == PARTICLE_IDS["Empty"]

        # If no empty space on top, right, or left, and grass has stopped moving
        if not (is_empty_above or is_empty_left or is_empty_right) and not has_moved:
            if random.random() < 0.005:  # 1% chance to turn into dirt
                grid[x][y] = Dirt()

class GrassSeed(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["GrassSeed"])
        self.color = random.choice([(107, 182, 41), (106, 177, 48)])

    def update(self, grid, x, y):
        if y < ROWS - 1:
            # Check directly below for gravity
            if grid[x][y + 1] == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            elif isinstance(grid[x][y + 1], Dirt):
                # Transform into Grass when hitting Dirt
                grid[x][y + 1] = create_particle(PARTICLE_IDS["Grass"])
                grid[x][y] = PARTICLE_IDS["Empty"]
                return  # Exit the method after transforming into Grass
            else:
                grid[x][y] = PARTICLE_IDS["Empty"]
                return
        elif y == ROWS - 1:
            grid[x][y] = PARTICLE_IDS["Empty"]

class TreeSeed(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["GrassSeed"])
        self.color = random.choice([(107, 182, 41), (106, 177, 48)])

    def update(self, grid, x, y):
        treeWidth = 7
        treeHeight = 7
        tree1 = [0, 0, 0, 2, 2, 2, 0, 
                 0, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 1, 2, 2, 2,
                 2, 2, 2, 1, 2, 2, 0,
                 0, 2, 2, 1, 0, 0, 0,
                 0, 0, 0, 1, 0, 0, 0,
                 0, 0, 0, 1, 0, 0, 0]
        tree2 = [0, 0, 0, 0, 0, 0, 0,
                 0, 0, 2, 2, 2, 0, 0,
                 0, 2, 2, 2, 2, 0, 0,
                 0, 2, 2 ,1, 2, 2, 0,
                 0, 2, 2, 1, 2, 2, 0,
                 0, 0, 0, 1, 2, 0, 0,
                 0, 0, 0, 1, 0, 0, 0]
        trees = [tree1, tree2]
        # 0 = EMPTY, 1 = WOOD, 2 = LEAF
        if y < ROWS - 1:
            # Check directly below for gravity
            if grid[x][y + 1] == PARTICLE_IDS["Empty"]:
                grid[x][y + 1], grid[x][y] = grid[x][y], PARTICLE_IDS["Empty"]
            elif isinstance(grid[x][y + 1], Dirt) or isinstance(grid[x][y + 1], Grass):
                grid[x][y] = PARTICLE_IDS["Empty"] # Delete Seed
                tree = random.choice(trees)
                for ty in range(treeHeight):
                    for tx in range(treeWidth):
                        tree_x = x + tx - (treeWidth // 2)
                        tree_y = y + ty - (treeHeight // 2) - 3  # Adjusted this line
                        if 0 <= tree_x < COLS and 0 <= tree_y < ROWS:  # Check grid boundaries
                            if tree[(ty * treeWidth) + tx] == 1:  # WOOD
                                grid[tree_x][tree_y] = create_particle(PARTICLE_IDS["Wood"])
                            elif tree[(ty * treeWidth) + tx] == 2:  # LEAF
                                grid[tree_x][tree_y] = create_particle(PARTICLE_IDS["Leaf"])
                return
            else:
                grid[x][y] = PARTICLE_IDS["Empty"]
                return
        elif y == ROWS - 1:
            # Disappear when reaching the bottom
            grid[x][y] = PARTICLE_IDS["Empty"]

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
        self.color = random.choice([(121, 59, 49), (126, 64, 54), (116, 54, 44), (124, 56, 52)])
    
    def update(self, grid, x, y):
        pass

class Wood(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Wood"])
        self.color = random.choice([(139, 97, 59), (133, 94, 66)])
    
    def update(self, grid, x, y):
        pass

class Leaf(Particle):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Leaf"])
        self.color = random.choice([(118, 175, 51), (137, 175, 51)])
    
    def update(self, grid, x, y):
        pass

class Acid(Liquid):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Acid"], density=0.5)
        self.color = (176, 191, 26)
        self.dissolve_probability = 0.03  # Probability to dissolve a block each frame

    def update(self, grid, x, y):
        reacted = False  # Flag to check if acid has reacted

        # Check all adjacent cells (above, below, left, right)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = x + dx, y + dy

            # Check if coordinates are within grid bounds
            if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                adjacent = grid[new_x][new_y]

                # If adjacent is not a brick, not empty, and not another liquid
                if adjacent != PARTICLE_IDS["Brick"] and adjacent != PARTICLE_IDS["Empty"] and not isinstance(adjacent, Acid):
                    # Random chance to dissolve the adjacent particle
                    if random.random() < self.dissolve_probability:
                        # Destroy the adjacent particle
                        grid[new_x][new_y] = PARTICLE_IDS["Empty"]
                        # Destroy itself
                        grid[x][y] = PARTICLE_IDS["Empty"]
                        return
                    reacted = True
                    break  # Stop checking further if reacted

        if not reacted:
            # If no reaction, behave like a normal liquid
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

class Smoke(Gas):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Smoke"])
        self.colors = [(224, 248, 255), (220, 245, 255), (216, 242, 255), (212, 239, 255)]
        self.color = random.choice(self.colors)
        self.move_delay = random.randint(8, 10)
        self.delay_counter = 0

    def update(self, grid, x, y):
        self.delay_counter += 1
        if self.delay_counter >= self.move_delay:
            self.delay_counter = 0
            self.color = random.choice(self.colors)
            super().update(grid, x, y)  # Use Gas class's update method

            # Eliminate smoke at the top
            if y == 0:
                grid[x][y] = PARTICLE_IDS["Empty"]

class Methane(Gas):
    def __init__(self):
        super().__init__(PARTICLE_IDS["Smoke"])
        self.colors = [(247, 211, 163), (245, 212, 169), (240, 207, 163), (245, 215, 171)]
        self.color = random.choice(self.colors)
        self.move_delay = random.randint(8, 10)
        self.delay_counter = 0
    
    def update(self, grid, x, y):
        self.delay_counter += 1
        if self.delay_counter >= self.move_delay:
            self.delay_counter = 0
            self.color = random.choice(self.colors)

            # Check adjacent cells including diagonals for fire
            adjacent_cells = [(0, -1), (0, 1), (-1, 0), (1, 0), # Up, Down, Left, Right
                            (-1, -1), (1, -1), (-1, 1), (1, 1)] # Diagonals: Left-Up, Right-Up, Left-Down, Right-Down
            for dx, dy in adjacent_cells:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < COLS and 0 <= new_y < ROWS:
                    if isinstance(grid[new_x][new_y], Fire):
                        grid[x][y] = create_particle(PARTICLE_IDS["Fire"])
                        return
            
            super().update(grid, x, y)

            if y == 0:
                grid[x][y] = PARTICLE_IDS["Empty"]

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
    elif particle_type_id == PARTICLE_IDS["Grass"]:
        return Grass()
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
    elif particle_type_id == PARTICLE_IDS["Methane"]:
        return Methane()
    elif particle_type_id == PARTICLE_IDS["GrassSeed"]:
        return GrassSeed()
    elif particle_type_id == PARTICLE_IDS["Wood"]:
        return Wood()
    elif particle_type_id == PARTICLE_IDS["Leaf"]:
        return Leaf()
    elif particle_type_id == PARTICLE_IDS["TreeSeed"]:
        return TreeSeed()
    else:
        print("UNKNOWN ID FOR CREATE PARTICLE COMMAND")
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