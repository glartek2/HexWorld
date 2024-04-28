import player
import pygame
import sys
from constant import BLACK, WHITE, screen_width, screen_height, scale, button_width, map_width, map_height
from draw_buttons import draw_button

pygame.font.init()

players = []
num_players = 2
# Define font
font = pygame.font.Font("resources/fonts/vinque rg.otf", 64)
map_width = map_width
map_height = map_height

# Create players
def create_players(num):
    for i in range(num):
        player_dummy = player.Player("Player" + str(i), i)
        players.append(player_dummy)


def update_players(num):
    global num_players
    num_players += num
    if num_players < 1:
        num_players = 1
    if num_players > 4:
        num_players = 4

def update_map_size(rows_change, cols_change):
    global map_width, map_height
    map_width += cols_change
    map_height += rows_change
    if map_width < 3:
        map_width = 3
    if map_height < 5:
        map_height = 5

# Function to display settings window
def settings(screen):
    while True:
        screen.fill(BLACK)

        # Draw "+" and "-" buttons for rows and columns
        minus_rows_rect = draw_button(screen, "-", "resources/buttons/button.png", screen_width // 3 - 150, screen_height // 4 - 50)
        plus_rows_rect = draw_button(screen, "+", "resources/buttons/button.png", screen_width * 2 // 3 - 50, screen_height // 4 - 50)
        minus_cols_rect = draw_button(screen, "-", "resources/buttons/button.png", screen_width // 3 - 150, screen_height // 3)
        plus_cols_rect = draw_button(screen, "+", "resources/buttons/button.png", screen_width * 2 // 3 - 50, screen_height // 3)

        # Draw "+" and "-" buttons for number of players
        minus_players_rect = draw_button(screen, "-", "resources/buttons/button.png", screen_width // 3 - 50, screen_height // 2 + 50)
        plus_players_rect = draw_button(screen, "+", "resources/buttons/button.png", screen_width * 2 // 3 - 150, screen_height // 2 + 50)

        # Draw number of rows and columns
        text_surface = font.render("Map Size", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4 - 100))
        screen.blit(text_surface, text_rect)

        text_surface = font.render("Columns: " + str(map_height), True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(text_surface, text_rect)

        text_surface = font.render("Rows: " + str(map_width), True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 3 + 50))
        screen.blit(text_surface, text_rect)

        # Draw number of players
        text_surface = font.render("Number of Players", True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        screen.blit(text_surface, text_rect)

        text_surface = font.render(str(num_players), True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(text_surface, text_rect)

        # Draw "Play" button
        play_button_rect = draw_button(screen, "Play", "resources/buttons/button.png",screen_width // 2 - 100, screen_height * 2 // 3)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if minus_rows_rect.collidepoint(mouse_x, mouse_y):
                    update_map_size(-1, 0)
                elif plus_rows_rect.collidepoint(mouse_x, mouse_y):
                    update_map_size(1, 0)
                elif minus_cols_rect.collidepoint(mouse_x, mouse_y):
                    update_map_size(0, -1)
                elif plus_cols_rect.collidepoint(mouse_x, mouse_y):
                    update_map_size(0, 1)
                elif minus_players_rect.collidepoint(mouse_x, mouse_y):
                    update_players(-1)
                elif plus_players_rect.collidepoint(mouse_x, mouse_y):
                    update_players(1)
                elif play_button_rect.collidepoint(mouse_x, mouse_y):
                    create_players(num_players)
                    return players

        pygame.display.flip()
