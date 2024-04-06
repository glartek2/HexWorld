import random

import pygame
import math
import numpy
from constant import *
from tile import Tile
import player as pl

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



# Create players
player1 = pl.Player("Player 1")
player2 = pl.Player("Player 2")
# Initialize turn counter
current_player = player1

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("CLick: ", mouse_x, mouse_y)
                # Iterate over the map grid to find the clicked tile
                for row in range(len(map_grid)):
                    for col in range(len(map_grid[row])):
                        tile = map_grid[row][col]
                        center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
                        center_x += int(tile_width/2 * scale)
                        center_y += int(tile_height//2 * scale)
                        print("Centrum: ", center_x, center_y)

                        # Check if the mouse position is within the bounds of the hexagon
                        if point_in_hexagon(mouse_x, mouse_y, center_x, center_y, tile_width * scale, tile_height * scale):
                            # Mouse click is within the bounds of the hexagon, consider it as clicked
                            print("Tile clicked at row:", row, "column:", col)
                            # Add code to handle tile selection here
                            break  # Stop checking other tiles if one is already clicked
                    else:
                        continue
                    break  # Exit outer loop if tile is found


    # Switch turns
    if current_player == player1:
        current_player = player2
    else:
        current_player = player1

    pygame.display.flip()
    clock.tick(60)


    # Function to check if a point is within a hexagon
    def point_in_hexagon(x, y, center_x, center_y, width, height):
        # Calculate the distances from the point to each side of the hexagon
        dx = abs(x - center_x)
        dy = abs(y - center_y)
        if dy > height / 2:
            return False
        return dx <= width / 2

pygame.quit()
