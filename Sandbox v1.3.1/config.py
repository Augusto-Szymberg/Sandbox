# Screen dimensions for multi-panel
center_panel_width = 800
center_panel_height = 800
left_panel_width = 150
right_panel_width = 190
screen_width = center_panel_width + left_panel_width + right_panel_width
screen_height = center_panel_height

# Particle IDs
PARTICLE_IDS = {
    "Empty": 0, "Sand": 1, "Water": 2, "Dirt": 3, "Grass": 4,
    "Stone": 5, "Brick": 6, "Acid": 7, "Oil": 8, "Fire": 9, 
    "Lava": 10, "BurningOil": 11, "Smoke": 12, "Methane": 13, 
    "GrassSeed": 14, "TreeSeed": 15, "Wood": 16, "Leaf": 17
}

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (211, 211, 211)
DARK_GREY = (169, 169, 169)

# Particle simulator constants
GRID_SIZE = 10
ROWS = center_panel_height // GRID_SIZE
COLS = center_panel_width // GRID_SIZE
BG_COLOR = (173, 216, 230)

# Particle selection button configuration
button_size = 50
grid_cols = 3
grid_rows = 2
button_margin = 10
start_x = left_panel_width + center_panel_width + button_margin
start_y = 50

# New variables for brush size and burst size radius
brush_size = 2  # The radius of the brush in grid cells
burst_size_radius = 2  # The radius of the burst size

def change_brush_size(new_brush_size, new_burst_size):
    global brush_size
    global burst_size_radius
    brush_size = new_brush_size
    burst_size_radius = new_burst_size

def get_brush_size():
    global brush_size
    return brush_size

def get_burst_size():
    global burst_size_radius
    return burst_size_radius
