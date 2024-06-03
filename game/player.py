from constant import positions, player_colors
import settings
from tile import find_neighbours

class Player:
    def __init__(self, name, player_number):
        self.name = name
        self.score = 0
        self.current_civ = None
        self.old_civ = None
        self.tiles = set()
        self.old_tiles = set()
        self.can_attack = set()
        self.current_attack_power = 0
        self.player_number = player_number
        self.player_color = player_colors[player_number]
        self.player_first_attack = True
        self.player_first_defence = True

    def update_tiles(self, tile):
        if tile in self.tiles:
            self.tiles.remove(tile)
            if self.current_civ and self.current_civ.species.death_handling():
                self.current_civ.number -= 1
            elif self.old_civ:
                self.old_civ.number -= 1
        else:
            self.tiles.add(tile)

    def attack(self, tile):
        if tile.terrain.isWater and not self.current_civ.species.can_attack_water():
            return 0

        bonus_attack_name, bonus_attack_value = self.current_civ.species.bonus_attack()
        if bonus_attack_name != tile.terrain:
            bonus_attack_value = 0

        self.score += self.current_civ.ability.bonus_score_on_attack()

        effective_attack_power = self.current_attack_power - max(tile.defence - bonus_attack_value, 1)
        if effective_attack_power >= 0:
            if self.player_first_attack and self.current_civ.ability.bonus_first_attack():
                self.current_attack_power -= 1
                self.player_first_attack = False
            else:
                self.current_attack_power = effective_attack_power
            return 1
        return 0

    def new_turn(self, map_grid, turn_counter):
        for row, col in self.tiles:
            tile = map_grid[row][col]
            tile.defence = tile.terrain.defence + 1

        self.player_first_attack = True
        self.player_first_defence = True

        if self.current_civ:
            self.current_attack_power = self.current_civ.number - len(self.tiles)

            if self.current_civ.ability.bonus_current_power() and turn_counter % 2 == 0:
                self.current_attack_power *= 2

            race_bonus_name, race_bonus_value = self.current_civ.species.bonus_attack_power()
            for row, col in self.tiles:
                tile = map_grid[row][col]
                if tile.terrain.name == race_bonus_name or tile.bonus.name == race_bonus_name:
                    self.current_attack_power += race_bonus_value
        else:
            self.current_attack_power = 0

    def extinction(self):
        if not self.current_civ.species.special_extinction():
            self.current_attack_power = 0
            self.old_tiles = self.tiles
            self.tiles = set()

        self.old_civ = self.current_civ
        self.current_civ = None
        self.can_attack = set()

    def update_civ(self, civ):
        self.current_civ = civ
        self.current_attack_power = civ.number
        map_height, map_width = settings.map_height, settings.map_width
        self.can_attack = {(i, j) for i in range(map_height) for j in range(map_width)}
        self.score += self.current_civ.ability.bonus_start_score()

    def update_can_attack(self):
        map_height, map_width = settings.map_height, settings.map_width
        if not self.tiles:
            self.can_attack = {(i, j) for i in range(map_height) for j in range(map_width)}
        else:
            can_attack_tiles = set()
            find_neighbours(can_attack_tiles, self.tiles, self.tiles)
            if self.current_civ.ability.is_flying():
                temp = set()
                find_neighbours(temp, can_attack_tiles, self.tiles)
                self.can_attack = temp
            else:
                self.can_attack = can_attack_tiles
