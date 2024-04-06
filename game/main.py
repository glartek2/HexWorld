import random

import pygame
import math
import numpy
from constant import *
from tile import Tile

# Set up Pygame
pygame.init()
pygame.display.set_caption("Hexagonal Map")
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


map_grid = [[None for _ in range(map_width)] for _ in range(map_height)]

# Fill map with tiles
count = 0
for i in range(map_height):
    for j in range(map_width):
        terrain = random.choice(Terrains)
        scaled_terrain_image = pygame.transform.scale(terrain.image, (tile_width * scale, tile_height * scale))
        map_grid[i][j] = Tile(i, j, terrain, random.choices(Bonuses, weights = weights_bonus)[0], scaled_terrain_image, count)
        count += 1


# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Draw tiles
    for row in map_grid:
        for tile in row:
            tile.draw(screen, offset_x, gap, offset_y)  # Pass the calculated offset

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
