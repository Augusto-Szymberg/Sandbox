# Screen dimensions for multi-panel
center_panel_width = 800
center_panel_height = 800
side_panel_width = 150
screen_width = center_panel_width + 2 * side_panel_width
screen_height = center_panel_height

# Particle IDs
PARTICLE_IDS = {
    "Empty": 0, "Sand": 1, "Water": 2, "Dirt": 3, 
    "Stone": 4, "Brick": 5, "Acid": 6, "Oil": 7, 
    "Fire": 8, "Lava": 9, "BurningOil": 10, "Smoke": 11
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
