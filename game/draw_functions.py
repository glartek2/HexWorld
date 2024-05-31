import pygame
import numpy as np
from constant import (
    button_height, button_width, BLACK, BROWN, WHITE,
    offset_x, offset_y, gap, tile_width, tile_height, scale,
    screen_width, screen_height
)

# Function to draw buttons with text and image
def draw_button(screen, text, image_path, x, y):
    font = pygame.font.Font("resources/fonts/VTCGoblinHand.ttf", 28)
    button_rect = pygame.Rect(x, y, button_width, button_height)

    # Load and scale image
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (button_width - 10, button_height - 10))

    # Draw image on button
    button_image_rect = image.get_rect(center=button_rect.center)
    screen.blit(image, button_image_rect)

    # Draw text on button
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect

# Function to draw circles on tiles
def draw_circle_on_tiles(screen, current_player, map_grid, tiles):
    for row_in, col_in in tiles:
        tile = map_grid[row_in][col_in]
        center_x, center_y = tile.get_x(offset_x, gap), tile.get_y(offset_y)
        center_x += int(tile_width / 2 * scale)
        center_y += int(tile_height // 2 * scale)

        pygame.draw.circle(screen, current_player.player_color, (center_x, center_y),
                           int(tile_width / 2 * scale), 3)

# Function to draw the extinction confirmation window
def draw_extinction_window(screen):
    # Draw window background
    pygame.draw.rect(screen, BROWN, (screen_width // 6, screen_height // 4, screen_width // 2, screen_height // 3))

    # Draw "Are you sure?" text
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Are you sure?", True, BLACK)
    text_rect = text_surface.get_rect(center=(screen_width // 4, screen_height // 3))
    screen.blit(text_surface, text_rect)

    # Draw "Yes" and "No" buttons
    yes_button_rect = draw_button(screen, "Yes", "resources/buttons/button.png", 300, 300)
    no_button_rect = draw_button(screen, "No", "resources/buttons/button.png", 500, 300)

    return yes_button_rect, no_button_rect

# Function to draw tiles
def draw_tiles(screen, map_grid):
    for row in map_grid:
        for tile in row:
            tile.draw(screen, offset_x, gap, offset_y)

# Function to create a hexagon shape surface
def create_hexagon_clip(surface, center_x, center_y, radius, R, G, B, color_diff=0):
    hexagon_points = [
        (center_x + radius * np.cos(angle), center_y + radius * np.sin(angle))
        for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False)
    ]
    pygame.draw.polygon(surface, (R, G, B, 150 - color_diff), hexagon_points)
    return surface

# Function to draw a single player's tile
def draw_single_player_tile(screen, map_grid, player, row_in, col_in, color_diff=0):
    tile = map_grid[row_in][col_in]
    center_x, center_y = tile.get_x(offset_x, gap), tile.get_y(offset_y)
    R, G, B = player.player_color
    surface = pygame.Surface((tile_width * scale, tile_height * scale), pygame.SRCALPHA)
    radius = min(tile_width * scale, tile_height * scale) / 2
    surface = create_hexagon_clip(surface, surface.get_width() / 2, surface.get_height() / 2,
                                  radius, R, G, B, color_diff)
    screen.blit(surface, (center_x, center_y))

# Function to draw all player tiles
def draw_player_tiles(screen, map_grid, players):
    for player in players:
        for row_in, col_in in player.tiles:
            draw_single_player_tile(screen, map_grid, player, row_in, col_in)
        for row_in, col_in in player.old_tiles:
            draw_single_player_tile(screen, map_grid, player, row_in, col_in, 70)

# Function to write text on the screen
def write_text(screen, text, font, pos_x, pos_y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (pos_x, pos_y))
