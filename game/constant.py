import bons
import terrain as t
import math
import pygame
import ability
import species

pygame.mixer.init()

# Generate map
tile_width = 508
tile_height = 442
map_width = 4
map_height = 12
scale = 0.25
screen_width, screen_height = 1200, 800


# Indexes of neighbours
positions = [(2, 0), (1, -1), (1, 0), (-2, 0), (-1, 0), (-1, -1)]


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
RED = (255, 0, 0)

player_colors = [BLUE, RED, GREEN, YELLOW]

# Load terrain images
Mountain_image = pygame.image.load("resources/terrains/mountain_snow.png")
Desert_image = pygame.image.load("resources/terrains/desert.png")
Field_image = pygame.image.load("resources/terrains/field.png")
Water_image = pygame.image.load("resources/terrains/water.png")
Forest_image = pygame.image.load("resources/terrains/forest.png")

# Define Terrains
Desert = t.Terrain("Desert", Desert_image, 2)
Field = t.Terrain("Field", Field_image, 2)
Water = t.Terrain("Water", Water_image, 2, isWater=True)
Mountain = t.Terrain("Mountain", Mountain_image, 3)
Forest = t.Terrain("Forest", Forest_image, 2)
Terrains = [Desert, Field, Water, Mountain, Forest]


#Load Bonuses Images
Mine_image = pygame.image.load("resources/bons/mine.png")
Fruits_image = pygame.image.load("resources/bons/fruits.png")
Magic_Source_image = pygame.image.load("resources/bons/magic_source.png")


# Define Bonuses
Fruits = bons.Bonus("Fruits", pygame.transform.scale(Fruits_image,
                            (Fruits_image.get_width() * scale, Fruits_image.get_height() * scale)))
Mine = bons.Bonus("Mine",pygame.transform.scale(Mine_image,
                            (Mine_image.get_width() * scale, Mine_image.get_height() * scale)))
Magic_Source = bons.Bonus("Magic_Source", pygame.transform.scale(Magic_Source_image,
                            (Magic_Source_image.get_width() * scale, Magic_Source_image.get_height() * scale)))

NoneBonus = bons.Bonus(None, None)
Bonuses = [Fruits, Mine, Magic_Source, NoneBonus]
weights_bonus = [2, 1, 1, 4]


# Simple Audio
pygame.mixer.music.load("resources/soundtrack/Basic_1_(Witcher).mp3")
attack_sound_1 = pygame.mixer.Sound("resources/soundtrack/Attack_1.mp3")
defence_sound_1 = pygame.mixer.Sound("resources/soundtrack/Defence_1.mp3")



# Button properties
button_width = 180
button_height = 120
button_spacing = 20
button_x = (map_width * 2 - 1) * tile_width * scale
attack_button_y = 100
defense_button_y = attack_button_y + button_height + button_spacing
extinction_button_y = defense_button_y + button_height + button_spacing
end_turn_button_y = extinction_button_y + button_height + button_spacing

button_positions = {
                "Attack": (button_x, attack_button_y),
                "Defence": (button_x, defense_button_y),
                "Extinct": (button_x, extinction_button_y),
                "END TURN": (button_x, end_turn_button_y)
                }



base_number_of_units = map_width * map_height // 4
base_scale = (map_width * map_height) // (4 * 12)

abilities = [
    ability.AbilityFactory.create_ability("Ancient", base_number_of_units),
    ability.AbilityFactory.create_ability("Flying", base_number_of_units // 2 * base_scale),
    ability.AbilityFactory.create_ability("Dino Tamers", base_number_of_units),
    ability.AbilityFactory.create_ability("Fortress", base_number_of_units - 4 * base_scale),
    ability.AbilityFactory.create_ability("Wealthy", base_number_of_units + 4 * base_scale),
    ability.AbilityFactory.create_ability("Victorious", base_number_of_units // 2 * ( base_scale)),
    ability.AbilityFactory.create_ability("Hungry", base_number_of_units - 2 * base_scale),
    ability.AbilityFactory.create_ability("Lykanous", base_number_of_units - 3 * base_scale)
]

species = [
    species.SpeciesFactory.create_species("Humans", base_number_of_units),
    species.SpeciesFactory.create_species("Dwarves", base_number_of_units // 2 * base_scale + 1 * base_scale),
    species.SpeciesFactory.create_species("Trytons", base_number_of_units),
    species.SpeciesFactory.create_species("Sorcerers", base_number_of_units // 2 * base_scale),
    species.SpeciesFactory.create_species("Beastmans", base_number_of_units - 1 * base_scale),
    species.SpeciesFactory.create_species("Giants", base_number_of_units - 2 * base_scale),
    species.SpeciesFactory.create_species("Elves", base_number_of_units - 1 * base_scale),
    species.SpeciesFactory.create_species("Ghouls", int(base_number_of_units * 2 // 1.5 * base_scale))
]
