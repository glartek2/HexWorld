from constant import tile_height, tile_width, weights_bonus, Bonuses, scale, Terrains
from constant import button_height, button_x, button_width, button_spacing
from constant import RED, GREEN, BLACK, BLUE, WHITE, BROWN, YELLOW, DARK_GREEN
from constant import attack_sound_1, defence_sound_1
import settings
from settings import players
import pygame
import random
import numpy as np
from tile import Tile


def create_map_grid():
    return [[None for _ in range(settings.map_width)] for _ in range(settings.map_height)]


# Fill map with tiles
def fill_map(map_grid):
    count = 0
    for i in range(settings.map_height):
        for j in range(settings.map_width):
            terrain = random.choice(Terrains)
            scaled_terrain_image = pygame.transform.scale(terrain.image, (tile_width * scale, tile_height * scale))
            map_grid[i][j] = Tile(i, j, terrain, random.choices(Bonuses, weights = weights_bonus)[0], scaled_terrain_image, count)
            count += 1



# Function to check if a point is within a hexagon
def point_in_hexagon(x, y, center_x, center_y, width, height):
    # Calculate the distances from the point to each side of the hexagon
    dx = abs(x - center_x)
    dy = abs(y - center_y)
    if dy > height / 2:
        return False
    return dx <= width / 2


def perform_attack(row, col, map_grid, current_player):
    if (row, col) in current_player.can_attack:
        if current_player.attack(map_grid[row][col]):
            pygame.mixer.Sound.play(attack_sound_1)
            update_players_after_attack(row, col, map_grid)

            current_player.update_tiles((row, col))
            current_player.update_can_attack()

def update_players_after_attack(row, col, map_grid):
    for player in players:
        if (row, col) in player.tiles:
            player.update_tiles((row, col))
            tile = map_grid[row][col]
            player.current_attack_power += tile.defence
            player.update_can_attack()


def perform_defence(row, col, map_grid, current_player):
    if (row, col) in current_player.tiles:
        if current_player.current_attack_power > 0:
            pygame.mixer.Sound.play(defence_sound_1)
            current_player.current_attack_power -= 1
            tile = map_grid[row][col]
            tile.defence += 1



def switch_turns(map_grid, current_player):
    next_player = players[(current_player.player_number + 1) % len(players)]
    next_player.new_turn(map_grid)
    return next_player