from constant import (
    tile_height, tile_width, weights_bonus, Bonuses, scale, Terrains,
    button_height, button_x, button_width, button_spacing,
    RED, GREEN, BLACK, BLUE, WHITE, BROWN, YELLOW, DARK_GREEN,
    attack_sound_1, defence_sound_1
)
import settings
from settings import players
import pygame
import random
import numpy as np
from tile import Tile


def create_map_grid():
    return [[None for _ in range(settings.map_width)] for _ in range(settings.map_height)]


def fill_map(map_grid):
    count = 0
    for i in range(settings.map_height):
        for j in range(settings.map_width):
            terrain = random.choice(Terrains)
            scaled_terrain_image = pygame.transform.scale(
                terrain.image, (tile_width * scale, tile_height * scale)
            )
            bonus = random.choices(Bonuses, weights=weights_bonus)[0]
            map_grid[i][j] = Tile(i, j, terrain, bonus, scaled_terrain_image, count)
            count += 1


def point_in_hexagon(x, y, center_x, center_y, width, height):
    dx = abs(x - center_x)
    dy = abs(y - center_y)
    return dy <= height / 2 and dx <= width / 2


def perform_attack(row, col, map_grid, current_player):
    if (row, col) in current_player.can_attack:
        tile = map_grid[row][col]
        if current_player.attack(tile):
            pygame.mixer.Sound.play(attack_sound_1)
            update_players_after_attack(row, col, map_grid)
            current_player.update_tiles((row, col))

            bonus_defence_name, bonus_defence_value = current_player.current_civ.species.bonus_defence()
            if bonus_defence_name == tile.terrain:
                tile.defence += bonus_defence_value

            current_player.update_can_attack()


def update_players_after_attack(row, col, map_grid):
    for player in players:
        if (row, col) in player.tiles:
            player.update_tiles((row, col))
            tile = map_grid[row][col]

            player.current_attack_power += tile.defence
            bonus_defence_name, bonus_defence_value = player.current_civ.species.bonus_defence()
            if bonus_defence_name == tile.terrain:
                tile.defence -= bonus_defence_value

            player.update_can_attack()


def perform_defence(row, col, map_grid, current_player):
    if (row, col) in current_player.tiles and current_player.current_attack_power > 0:
        pygame.mixer.Sound.play(defence_sound_1)
        current_player.current_attack_power -= 1
        tile = map_grid[row][col]

        bonus_defence_ability, flag = current_player.current_civ.ability.bonus_defence()
        bonus_terrain_name, bonus_defence_species = current_player.current_civ.species.bonus_defence()
        if flag:
            if current_player.player_first_defence:
                tile.defence += 1 + bonus_defence_ability
                current_player.player_first_defence = False
            else:
                tile.defence += 1
        else:
            tile.defence += 1 + bonus_defence_ability

        if tile.terrain.name == bonus_terrain_name:
            tile.defence += bonus_defence_species


def switch_turns(map_grid, current_player, turn_counter):
    next_player = players[(current_player.player_number + 1) % len(players)]
    next_player.new_turn(map_grid, turn_counter//len(players))
    return next_player
