from config import ROWS, COLS
from particles import Particle

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