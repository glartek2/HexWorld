from constant import tile_height, tile_width, weights_bonus, Bonuses, scale, Terrains
from constant import button_height, button_x, button_width, button_spacing
from constant import RED, GREEN, BLACK, BLUE, WHITE, BROWN, YELLOW, DARK_GREEN
import settings
from settings import players
import pygame
import random
import numpy as np
from tile import Tile


# Fill map with tiles
def fill_map(map_grid):
    count = 0
    for i in range(settings.map_height):
        for j in range(settings.map_width):
            terrain = random.choice(Terrains)
            scaled_terrain_image = pygame.transform.scale(terrain.image, (tile_width * scale, tile_height * scale))
            map_grid[i][j] = Tile(i, j, terrain, random.choices(Bonuses, weights = weights_bonus)[0], scaled_terrain_image, count)
            count += 1




# Create hexagon shape surface (to show players tiles)
def create_hexagon_clip(surface, center_x, center_y, radius, R, G, B):
    hexagon_points = [(center_x + radius * np.cos(angle),
                       center_y + radius * np.sin(angle)) for angle in np.linspace(0, 2*np.pi, 6, endpoint=False)]
    pygame.draw.polygon(surface, (R, G, B, 100), hexagon_points)
    return surface




# Function to check if a point is within a hexagon
def point_in_hexagon(x, y, center_x, center_y, width, height):
    # Calculate the distances from the point to each side of the hexagon
    dx = abs(x - center_x)
    dy = abs(y - center_y)
    if dy > height / 2:
        return False
    return dx <= width / 2



def switch_turns(current_player):
    next_player = players[(current_player.player_number + 1) % len(players)]
    next_player.new_turn()
    return next_player