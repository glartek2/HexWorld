import pygame
import math
import constant as con

class Tile:
    def __init__(self, row, col, terrain, bon, image, num):
        self.row = row
        self.col = col
        self.terrain = terrain
        self.bon = bon
        self.image = image
        self.num = num
        self.defence = terrain.defence

    def getX(self, x_offset, gap):
        image_width = self.image.get_rect().width
        if self.row % 2 == 0:
            fudge_factor = self.col * 2 + 2
            return int((x_offset + self.col * (image_width + gap) - fudge_factor))
        else:
            fudge_factor = self.col * 2
            return int((self.col * (image_width + gap) - fudge_factor))

    def getY(self, height_adjust):
        return int((self.row * height_adjust))

    def draw(self, screen, x_offset, gap, height_adjust):
        x = self.getX(x_offset, gap)
        y = self.getY(height_adjust)

        screen.blit(self.image, (x, y))

        # Draw bonus (if any)
        if self.bon != con.NoneBonus:
            bon_rect = self.bon.image.get_rect(center=(x + self.image.get_width() / 2, y + self.image.get_height() / 2))
            screen.blit(self.bon.image, bon_rect)

        # Draw the number
        font = pygame.font.Font(None, 36)  # You can change the font and size as needed
        text_surface = font.render(str(self.num), True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(x + self.image.get_width() / 2, y + self.image.get_height() / 2))
        screen.blit(text_surface, text_rect)

    def update_defence(self, bonus_defence):
        self.defence = self.terrain.defence + bonus_defence
