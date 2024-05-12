from constant import positions, player_colors
import settings


class Player:
    def __init__(self, name, player_number):
        self.name = name                                    # Player Name
        self.score = 0                                      # Player Score
        self.current_civ = None                             # Player's current civilization
        self.old_civ = None                                 # Player's last civilization
        self.tiles = set()                                  # Player's tiles - map indexes
        self.old_tiles = set()                              # Old civilization tiles
        self.can_attack = set()                             # Tiles that player can attack
        self.current_attack_power = 0
        self.player_number = player_number
        self.player_color = player_colors[player_number]



    def update_tiles(self, tile):
        # Add or remove tile

        if tile in self.tiles:
            self.tiles.remove(tile)
            if self.current_civ:
                self.current_civ.number -= 1
            else:
                self.old_civ.number -= 1
        else:
            self.tiles.add(tile)


    def attack(self, tile):
        if tile.terrain.isWater and not self.current_civ.spieces.can_attack_water():
            return 0
        if self.current_attack_power >= tile.defence:
            self.current_attack_power -= tile.defence
            return 1
        return 0



    def new_turn(self, map_grid):

        for row_in, col_in in self.tiles:
            tile = map_grid[row_in][col_in]
            tile.defence = tile.terrain.defence + 1

        try:
            self.current_attack_power = self.current_civ.number - len(self.tiles)
        except AttributeError:
            self.current_attack_power = 0


    def extinction(self):
        # set spieces as extinct

        self.old_civ = self.current_civ
        self.current_civ = None
        self.old_tiles = self.tiles
        self.tiles = set()
        self.current_attack_power = 0
        self.can_attack = set()

    def update_civ(self, civ):
        # set new civ

        self.current_civ = civ
        self.current_attack_power = civ.number
        map_height = settings.map_height
        map_width = settings.map_width
        self.can_attack = set((i, j) for i in range(map_height) for j in range(map_width))


    def update_can_attack(self):
        # update list of possible tiles to attack
        map_height = settings.map_height
        map_width = settings.map_width
        if len(self.tiles) == 0:
            self.can_attack = set((i, j) for i in range(map_height) for j in range(map_width))
        else:
            self.can_attack = set()
            for tile in self.tiles:
                if tile[0] % 2 == 0:
                    is_even = -1
                else:
                    is_even = 1

                for pos in positions:
                    x = tile[0] + pos[0] * is_even
                    y = tile[1] + pos[1] * is_even
                    if 0 <= x < map_height and 0 <= y < map_width and (x, y) not in self.tiles:
                        self.can_attack.add((x, y))