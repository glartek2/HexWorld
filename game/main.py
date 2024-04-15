import random

import pygame
import math
import numpy
from constant import *
from tile import Tile
import player as pl

# Set up Pygame
pygame.init()
pygame.display.set_caption("Hexagonal Map")
screen = pygame.display.set_mode((screen_width, screen_height))


map_grid = [[None for _ in range(map_width)] for _ in range(map_height)]

# Fill map with tiles
count = 0
for i in range(map_height):
    for j in range(map_width):
        terrain = random.choice(Terrains)
        scaled_terrain_image = pygame.transform.scale(terrain.image, (tile_width * scale, tile_height * scale))
        map_grid[i][j] = Tile(i, j, terrain, random.choices(Bonuses, weights = weights_bonus)[0], scaled_terrain_image, count)
        count += 1



# Create players
player1 = pl.Player("Player 1", 0)
player2 = pl.Player("Player 2", 1)
players = [player1, player2]
print(player2.player_color)
# Initialize turn counter
current_player = player1


# Button properties
button_width = 180
button_height = 120
button_spacing = 20
button_x = (map_width * 2 - 1) * tile_width * scale
attack_button_y = 20
defense_button_y = attack_button_y + button_height + button_spacing
extinction_button_y = defense_button_y + button_height + button_spacing
end_turn_button_y = extinction_button_y + button_height + button_spacing

# Function to draw buttons
# Function to draw buttons with text and image
def draw_button(text, image_path, x, y):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, button_width, button_height)
    #pygame.draw.rect(screen, BLACK, button_rect, 2)

    # Load image
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (button_width - 10, button_height - 10))  # Adjust size if needed

    # Draw image on button surface
    button_image_rect = image.get_rect(center=button_rect.center)
    screen.blit(image, button_image_rect)

    # Draw text on button
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect


def switch_turns():
    return players[(current_player.player_number + 1) % len(players)]


# TEST:
current_player.update_tiles((1, 1))
current_player.update_can_attack()
print(current_player.can_attack)


player2.update_tiles((5, 3))
print(player2.tiles)
player2.update_can_attack()


# Main loop
running = True
confirm_extinction = False
attack_clicked = False


while running:
    screen.fill(BLACK)

    # Draw buttons
    attack_button_rect = draw_button("Attack", "resources/buttons/attack_button.png", button_x, attack_button_y)
    defense_button_rect = draw_button("Defense", "resources/buttons/defence_button.png", button_x, defense_button_y)
    extinction_button_rect = draw_button("Extinction", "resources/buttons/extinction_button.png", button_x,
                                         extinction_button_y)
    end_turn_button_rect = draw_button("END TURN", "resources/buttons/end_turn_button.png", button_x, end_turn_button_y)

    # Draw tiles
    for row in map_grid:
        for tile in row:
            tile.draw(screen, offset_x, gap, offset_y)  # Pass the calculated offset



    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:  # Left mouse button clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if attack_button_rect.collidepoint(mouse_x, mouse_y):
                    attack_clicked = not attack_clicked

                elif defense_button_rect.collidepoint(mouse_x, mouse_y):

                    print("Defense action triggered")
                elif extinction_button_rect.collidepoint(mouse_x, mouse_y):
                    # Set the flag to display the confirmation window
                    confirm_extinction = True

                elif confirm_extinction:
                    # If confirmation window is displayed, check if "Yes" or "No" button is clicked
                    if yes_button_rect.collidepoint(mouse_x, mouse_y):
                        # Perform extinction action
                        print("Extinction action confirmed")
                        confirm_extinction = False

                    elif no_button_rect.collidepoint(mouse_x, mouse_y):
                        # Cancel extinction action
                        print("Extinction action canceled")
                        confirm_extinction = False

                elif end_turn_button_rect.collidepoint(mouse_x, mouse_y):

                    current_player = switch_turns()
                    attack_clicked = False


                else:
                    # Iterate over the map grid to find the clicked tile
                    for row in range(len(map_grid)):
                        for col in range(len(map_grid[row])):
                            tile = map_grid[row][col]
                            center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
                            center_x += int(tile_width/2 * scale)
                            center_y += int(tile_height//2 * scale)

                            # Check if the mouse position is within the bounds of the hexagon
                            if point_in_hexagon(mouse_x, mouse_y, center_x, center_y, tile_width * scale, tile_height * scale):
                                # Mouse click is within the bounds of the hexagon, consider it as clicked

                                if attack_clicked:
                                    if (row, col) in current_player.can_attack:
                                        current_player.update_tiles((row, col))
                                        current_player.update_can_attack()
                                        print(current_player.can_attack)

                                #print(current_player.name)
                                print("Tile clicked at row:", row, "column:", col)

                                break  # Stop checking other tiles if one is already clicked
                        else:
                            continue
                        break  # Exit outer loop if tile is found

    if attack_clicked:
        for row_in, col_in in current_player.can_attack:

            tile = map_grid[row_in][col_in]
            center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
            center_x += int(tile_width / 2 * scale)
            center_y += int(tile_height // 2 * scale)

            pygame.draw.circle(screen, current_player.player_color, (center_x, center_y), int(tile_width / 2 * scale), 3)



    # Draw confirmation window if flag is set
    if confirm_extinction:
        # Draw confirmation window background
        pygame.draw.rect(screen, BROWN, (screen_width//6, screen_height//4, screen_width//2, screen_height//3))

        #Draw "Are you sure?" text
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Are you sure?", True, BLACK)
        text_rect = text_surface.get_rect(center=(screen_width // 4, screen_height // 3))
        screen.blit(text_surface, text_rect)

        # Draw "Yes" and "No" buttons
        yes_button_rect = draw_button("Yes", "resources/buttons/button.png", 300, 300)
        no_button_rect = draw_button("No", "resources/buttons/button.png", 500, 300)


    pygame.display.flip()


    # Function to check if a point is within a hexagon
    def point_in_hexagon(x, y, center_x, center_y, width, height):
        # Calculate the distances from the point to each side of the hexagon
        dx = abs(x - center_x)
        dy = abs(y - center_y)
        if dy > height / 2:
            return False
        return dx <= width / 2

pygame.quit()
