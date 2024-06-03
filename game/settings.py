import player
import pygame
import sys
from constant import BLACK, WHITE, screen_width, screen_height, map_width, map_height
from draw_functions import draw_button, write_text

pygame.font.init()

players = []
num_players = 2
player_names = ["Player1", "Player2"]
input_boxes = []

# Define font
font = pygame.font.Font("resources/fonts/vinque rg.otf", 64)
input_font = pygame.font.Font(None, 32)
map_width = map_width
map_height = map_height

# TextInputBox class
class TextInputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.txt_surface = input_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = input_font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


# Create players with names
def create_players(names):
    for i, name in enumerate(names):
        player_dummy = player.Player(name, i)
        players.append(player_dummy)


def update_players(num):
    global num_players, player_names, input_boxes
    num_players += num
    if num_players < 1:
        num_players = 1
    if num_players > 4:
        num_players = 4

    # Adjust player names and input boxes
    player_names = player_names[:num_players] + ["Player" + str(i) for i in range(len(player_names), num_players)]
    input_boxes = input_boxes[:num_players] + [
        TextInputBox(screen_width // 2 - 100, screen_height // 2 + 150 + i*40, 140, 32,
                     player_names[i]) for i in range(len(input_boxes), num_players)]


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
    global player_names
    update_players(0)  # Initialize player input boxes

    while True:
        screen.fill(BLACK)

        # Draw "+" and "-" buttons for rows and columns
        minus_rows_rect = draw_button(screen, "-", "resources/buttons/button.png",
                                      screen_width // 3 - 150, screen_height // 4 - 50)
        plus_rows_rect = draw_button(screen, "+", "resources/buttons/button.png",
                                     screen_width * 2 // 3 - 50, screen_height // 4 - 50)
        minus_cols_rect = draw_button(screen, "-", "resources/buttons/button.png",
                                      screen_width // 3 - 150, screen_height // 3)
        plus_cols_rect = draw_button(screen, "+", "resources/buttons/button.png",
                                     screen_width * 2 // 3 - 50, screen_height // 3)

        # Draw "+" and "-" buttons for number of players
        minus_players_rect = draw_button(screen, "-", "resources/buttons/button.png",
                                         screen_width // 3 - 50, screen_height // 2 + 50)
        plus_players_rect = draw_button(screen, "+", "resources/buttons/button.png",
                                        screen_width * 2 // 3 - 150, screen_height // 2 + 50)

        # Draw number of rows and columns
        write_text(screen, "Map Size", font, screen_width // 2, screen_height // 4 - 100)
        write_text(screen, "Columns:" + str(map_height), font, screen_width // 2, screen_height // 4)
        write_text(screen, "Rows: " + str(map_width), font, screen_width // 2, screen_height // 3 + 50)
        write_text(screen, "Number of Players", font, screen_width // 2, screen_height // 2 + 20)
        write_text(screen, str(num_players), font, screen_width // 2, screen_height // 2 + 100)

        # Draw player name input boxes
        for i, box in enumerate(input_boxes):
            box.draw(screen)

        # Draw "Play" button
        play_button_rect = draw_button(screen, "Play", "resources/buttons/button.png",
                                       screen_width // 2 - 100, screen_height * 5 // 6 + 10)

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
                    for i, box in enumerate(input_boxes):
                        player_names[i] = box.text
                    create_players(player_names[:num_players])
                    return players
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        pygame.display.flip()


