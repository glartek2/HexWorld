import pygame
import math
import constant as con


class Tile:
    def __init__(self, row, col, terrain, bonus, image, num):
        self.row = row
        self.col = col
        self.terrain = terrain
        self.bonus = bonus
        self.image = image
        self.num = num
        self.defence = terrain.defence


    def get_x(self, x_offset, gap):
        image_width = self.image.get_rect().width
        if self.row % 2 == 0:
            fudge_factor = self.col * 2 + 2
            return int((x_offset + self.col * (image_width + gap) - fudge_factor))
        else:
            fudge_factor = self.col * 2
            return int((self.col * (image_width + gap) - fudge_factor))

    def get_y(self, height_adjust):
        return int((self.row * height_adjust))

    def draw(self, screen, x_offset, gap, height_adjust):
        x = self.get_x(x_offset, gap)
        y = self.get_y(height_adjust)

        screen.blit(self.image, (x, y))

        # Draw bonus (if any)
        if self.bonus != con.NoneBonus:
            bon_rect = self.bonus.image.get_rect(center=(x + self.image.get_width() / 2,
                                                         y + self.image.get_height() / 2))
            screen.blit(self.bonus.image, bon_rect)

        font = pygame.font.Font(None, 56)
        text_surface = font.render(str(self.defence), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + self.image.get_width() / 2,
                                                  y + self.image.get_height() / 2))
        screen.blit(text_surface, text_rect)

    def update_defence(self, bonus_defence):
        self.defence = self.terrain.defence + bonus_defence


def find_neighbours(neighbours, tiles, player_tiles):
    for tile in tiles:
        if tile[0] % 2 == 0:
            is_even = -1
        else:
            is_even = 1

        for pos in con.positions:
            x = tile[0] + pos[0] * is_even
            y = tile[1] + pos[1] * is_even
            if 0 <= x < con.map_height and 0 <= y < con.map_width and (x, y) not in player_tiles:
                neighbours.add((x, y))
