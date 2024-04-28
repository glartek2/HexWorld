from constant import *      # I know it doesn't look good, but they just variables that I don't want in main
import main_menu
import civilization
import spieces
import abilities
import functions as func
import settings
import score_system as ss
from draw_buttons import draw_button

# Set up Pygame
pygame.init()
pygame.display.set_caption("Hexagonal Map")
screen = pygame.display.set_mode((screen_width, screen_height))


players = []

# TEST
simple_spieces = spieces.Spieces(7)
simple_ability = abilities.Abilities(4)

simple_civ = civilization.Civ(simple_spieces, simple_ability)

simple_spieces_2 = spieces.Spieces(7)
simple_ability_2 = abilities.Abilities(4)

simple_civ_2 = civilization.Civ(simple_spieces_2, simple_ability_2)

simple_spieces_3 = spieces.Spieces(7)
simple_ability_3 = abilities.Abilities(4)

simple_civ_3 = civilization.Civ(simple_spieces_3, simple_ability_3)

simple_spieces_4 = spieces.Spieces(7)
simple_ability_4 = abilities.Abilities(4)

simple_civ_4 = civilization.Civ(simple_spieces_4, simple_ability_4)

civs = [simple_civ, simple_civ_2, simple_civ_3, simple_civ_4]

# END TEST


# Main loop
running = True
confirm_extinction = False
attack_clicked = False
defense_clicked = False
can_extinct = True
map_to_create = True


# Define game states
MAIN_MENU = 0
SETTINGS = 1
GAME = 2


# Initial game state
current_state = MAIN_MENU

while running:

    if current_state == MAIN_MENU:
        main_menu.main_menu(screen)
        current_state = SETTINGS  # Change state to settings after exiting main menu

    elif current_state == SETTINGS:
        players = settings.settings(screen)
        current_player = players[0]
        for idx, player in enumerate(players):
            player.update_civ(civs[idx])
            player.update_tiles((idx, idx))
            player.update_can_attack()
        current_state = GAME  # Change state to game after exiting settings

    elif current_state == GAME:
        if map_to_create:
            map_grid = [[None for _ in range(settings.map_width)] for _ in
                        range(settings.map_height)]  # initiate game map (matrix)

            func.fill_map(map_grid)
            map_to_create = False

        screen.fill(BLACK)

        # Draw buttons
        attack_button_rect = draw_button(screen, "Attack", "resources/buttons/attack_button.png",
                                         button_x, attack_button_y)

        defense_button_rect = draw_button(screen, "Defense", "resources/buttons/defence_button.png",
                                          button_x, defense_button_y)

        if can_extinct:
            extinction_button_rect = draw_button(screen, "Extinct", "resources/buttons/extinction_button.png",
                                                 button_x, extinction_button_y)
        else:
            extinction_button_rect = draw_button(screen, "Extinct", "resources/buttons/extinction_button_non_active.png",
                                                 button_x, extinction_button_y)

        end_turn_button_rect = draw_button(screen, "END TURN", "resources/buttons/end_turn_button.png",
                                           button_x, end_turn_button_y)

        # End buttons

        font = pygame.font.Font("resources/fonts/vinque rg.otf", 24)
        score_text = font.render(f"Current Player Score: {current_player.score}", True, WHITE)
        screen.blit(score_text, ((map_width * 2 - 1) * tile_width * scale - 50, 10))  # Adjust the position as needed

        score_text = font.render(f"Current Player Attack Power: {current_player.current_attack_power}", True, WHITE)
        screen.blit(score_text, ((map_width * 2 - 1) * tile_width * scale - 50, 50))

        # Draw tiles
        for row in map_grid:
            for tile in row:
                tile.draw(screen, offset_x, gap, offset_y)  # Pass the calculated offset

        for player in players:
            for row_in, col_in in player.tiles:
                tile = map_grid[row_in][col_in]
                center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
                #center_x += int(tile_width / 2 * scale)
                #center_y += int(tile_height // 2 * scale)
                R, G, B = player.player_color
                surface = pygame.Surface((tile_width * scale, tile_height * scale), pygame.SRCALPHA)
                radius = min(tile_width * scale, tile_height * scale) / 2
                surface = func.create_hexagon_clip(surface, surface.get_width() / 2, surface.get_height() / 2, radius, R, G, B)
                #surface.fill((R, G, B, 100))

                # Create a clipping region
                radius = min(tile_width * scale, tile_height * scale) / 2
                #surface = create_hexagon_clip(surface, surface.get_width() / 2, surface.get_height() / 2, radius)

                screen.blit(surface, (center_x, center_y))
                #pygame.draw.circle(screen, (R, G, B, 70), (center_x, center_y), int(tile_width / 2 * scale), 3)



        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  # Left mouse button clicked
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if attack_button_rect.collidepoint(mouse_x, mouse_y):
                        attack_clicked = not attack_clicked
                        can_extinct = False

                    elif defense_button_rect.collidepoint(mouse_x, mouse_y):
                        defense_clicked = not defense_clicked
                        can_extinct = False

                    elif extinction_button_rect.collidepoint(mouse_x, mouse_y):
                        # Set the flag to display the confirmation window
                        if can_extinct:
                            confirm_extinction = True

                    elif confirm_extinction:
                        # If confirmation window is displayed, check if "Yes" or "No" button is clicked
                        if yes_button_rect.collidepoint(mouse_x, mouse_y):
                            # Perform extinction action
                            print("Extinction action confirmed")
                            current_player.extinction()
                            confirm_extinction = False

                        elif no_button_rect.collidepoint(mouse_x, mouse_y):
                            # Cancel extinction action
                            print("Extinction action canceled")
                            confirm_extinction = False

                    elif end_turn_button_rect.collidepoint(mouse_x, mouse_y):

                        ss.update_score(current_player)
                        current_player = func.switch_turns(current_player)
                        for row_in, col_in in current_player.tiles:
                            tile = map_grid[row_in][col_in]
                            tile.defence = tile.terrain.defence + 1
                        attack_clicked = False
                        can_extinct = True


                    else:
                        # Iterate over the map grid to find the clicked tile
                        for row in range(len(map_grid)):
                            for col in range(len(map_grid[row])):
                                tile = map_grid[row][col]
                                center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
                                center_x += int(tile_width/2 * scale)
                                center_y += int(tile_height//2 * scale)

                                # Check if the mouse position is within the bounds of the hexagon
                                if func.point_in_hexagon(mouse_x, mouse_y, center_x, center_y, tile_width * scale, tile_height * scale):
                                    # Mouse click is within the bounds of the hexagon, consider it as clicked

                                    if attack_clicked:
                                        if (row, col) in current_player.can_attack:
                                            if current_player.attack(map_grid[row][col]):
                                                for player in players:
                                                    if (row, col) in player.tiles:
                                                        player.update_tiles((row, col))
                                                        tile = map_grid[row][col]
                                                        player.current_attack_power += tile.defence
                                                        player.update_can_attack()

                                                current_player.update_tiles((row, col))
                                                current_player.update_can_attack()

                                    elif defense_clicked:
                                        if (row, col) in current_player.tiles:
                                            if current_player.current_attack_power > 0:
                                                current_player.current_attack_power -= 1
                                                tile = map_grid[row][col]
                                                tile.defence += 1

                                    break  # Stop checking other tiles if one is already clicked
                            else:
                                continue
                            break  # Exit outer loop if tile is found


        # Check if attack button is pressed
        if attack_clicked:
            for row_in, col_in in current_player.can_attack:

                tile = map_grid[row_in][col_in]
                center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
                center_x += int(tile_width / 2 * scale)
                center_y += int(tile_height // 2 * scale)

                pygame.draw.circle(screen, current_player.player_color, (center_x, center_y), int(tile_width / 2 * scale), 3)

        # Check if defence button is pressed
        if defense_clicked:
            for row_in, col_in in current_player.tiles:
                tile = map_grid[row_in][col_in]
                center_x, center_y = tile.getX(offset_x, gap), tile.getY(offset_y)
                center_x += int(tile_width / 2 * scale)
                center_y += int(tile_height // 2 * scale)

                pygame.draw.circle(screen, current_player.player_color, (center_x, center_y),
                                   int(tile_width / 2 * scale), 3)


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
            yes_button_rect = draw_button(screen, "Yes", "resources/buttons/button.png", 300, 300)
            no_button_rect = draw_button(screen, "No", "resources/buttons/button.png", 500, 300)


        #if not current_player.current_civ:
            #print("Fast test to check if player has current spiece")

        pygame.display.flip()

pygame.quit()
