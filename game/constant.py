import bons
import terrain as t
import math
import pygame


# Generate map
tile_width = 508
tile_height = 442
map_width = 4
map_height = 12
scale = 0.25
screen_width, screen_height = 1200, 800


# Indexes of neighbours
positions = [-2*map_width, -(map_width+1), map_width+1, 2*map_width, map_width, -map_width]


# Calculate offset to center the map within the window
map_width_px = map_width * tile_width * 1.5
map_height_px = map_height * tile_height * math.sqrt(3) + (map_width % 2) * tile_height * math.sqrt(3) / 2
# Measure by hand
offset_x = 385 * scale
offset_y = 221 * scale
gap = 258 * scale # gap between hexes


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
DARK_GREEN = (10, 90, 10)

# Load terrain images
Mountain_image = pygame.image.load("resources/terrains/mountain_snow.png")
Desert_image = pygame.image.load("resources/terrains/desert.png")
Field_image = pygame.image.load("resources/terrains/field.png")
Water_image = pygame.image.load("resources/terrains/water.png")
Forest_image = pygame.image.load("resources/terrains/forest.png")

# Define Terrains
Desert = t.Terrain(Desert_image, 2)
Field = t.Terrain(Field_image, 2)
Water = t.Terrain(Water_image, 2, isWater=True)
Mountain = t.Terrain(Mountain_image, 3)
Forest = t.Terrain(Forest_image, 2)
Terrains = [Desert, Field, Water, Mountain, Forest]


# Define Bonuses
Fruits = bons.Bonus("Fruits")
Mine = bons.Bonus("Mine")
Magic_Source = bons.Bonus("Magic Source")
NoneBonus = bons.Bonus("None")
Bonuses = [Fruits, Mine, Magic_Source, NoneBonus]
weights_bonus = [2, 1, 1, 4]