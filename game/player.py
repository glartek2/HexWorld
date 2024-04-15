import tile
from constant import positions, map_width, map_height, player_colors
import civilization

class Player:
    def __init__(self, name, player_number):
        self.name = name                # Player Name
        self.score = 0                  # Player Score
        self.current_civ = None         # Player's current civilization
        self.old_civ = None             # Player's last civilization
        self.tiles = set()              # Player's tiles - map indexes
        self.can_attack = set()         # Tiles that player can attack
        self.player_number = player_number
        self.player_color = player_colors[player_number]



    def update_tiles(self, tile):
        # Add or remove tile

        if tile in self.tiles:
            self.tiles.remove(tile)
        else:
            self.tiles.add(tile)

    def extinction(self):
        # set spieces as extinct

        self.old_civ = self.current_civ
        self.current_civ = None
        self.can_attack = set()

    def update_spieces_and_ability(self, civ):
        # set new spieces

        self.current_civ = civ
        self.can_attack = set((i, j) for i in range(map_width) for j in range(map_height))


    def update_can_attack(self):
        # update list of possible tiles to attack
        self.can_attack = set()
        for tile in self.tiles:
            if tile[0] % 2 == 0:
                is_even = -1
            else:
                is_even = 1

            for pos in positions:
                x = tile[0] + pos[0] * is_even
                y = tile[1] + pos[1] * is_even
                if x >= 0 and x < map_height and y >= 0 and y < map_width and (x, y) not in self.tiles:
                    self.can_attack.add((x, y))

        #self.can_attack = set((((tile[0]*map_width+tile[1]) + pos) // map_width, ((tile[0]*map_width+tile[1]) + pos) % map_width) for tile in self.tiles for pos in positions)