import pygame.mixer

import constant as cn
import main_menu
import civilization
import spieces
import abilities
import functions as func
import settings
import score_system as ss
import draw_functions as draw

# Set up Pygame
pygame.init()
pygame.display.set_caption("Hexagonal Map")
screen = pygame.display.set_mode((cn.screen_width, cn.screen_height))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

font = pygame.font.Font("resources/fonts/vinque rg.otf", 24)

players = []

# TEST
simple_spieces = spieces.Spieces(7)
simple_ability = abilities.Abilities(4)

simple_civ = civilization.Civilization(simple_spieces, simple_ability)

simple_spieces_2 = spieces.Spieces(7)
simple_ability_2 = abilities.Abilities(4)

simple_civ_2 = civilization.Civilization(simple_spieces_2, simple_ability_2)

simple_spieces_3 = spieces.Spieces(7)
simple_ability_3 = abilities.Abilities(4)

simple_civ_3 = civilization.Civilization(simple_spieces_3, simple_ability_3)

simple_spieces_4 = spieces.Spieces(7)
simple_ability_4 = abilities.Abilities(4)

simple_civ_4 = civilization.Civilization(simple_spieces_4, simple_ability_4)

civs = [simple_civ, simple_civ_2, simple_civ_3, simple_civ_4]


# END TEST


def main_loop():
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
            # Test
            for idx, player in enumerate(players):
                player.update_civ(civs[0])
                player.update_tiles((idx, idx))
                player.update_can_attack()
            # Test

            current_state = GAME  # Change state to game after exiting settings

        elif current_state == GAME:
            if map_to_create:
                map_grid = func.create_map_grid()  # initiate game map (matrix)

                func.fill_map(map_grid)
                map_to_create = False

            screen.fill(cn.BLACK)

            # Draw buttons

            button_images = {
                "Attack": "resources/buttons/attack_button.png",
                "Defence": "resources/buttons/defence_button.png",
                "Extinct": "resources/buttons/extinction_button.png" if can_extinct
                else "resources/buttons/extinction_button_non_active.png",
                "END TURN": "resources/buttons/end_turn_button.png"
            }

            button_rects = {}
            for button_name, (pos_x, pos_y) in cn.button_positions.items():
                button_image = button_images[button_name]
                button_rects[button_name] = draw.draw_button(screen, button_name, button_image, pos_x, pos_y)

            # End buttons


            # Write score
            draw.write_text(screen, f"Score: {current_player.score}", font,
                            (cn.map_width * 2 - 1) * cn.tile_width * cn.scale - 50, 10)
            # Write current player attack power
            draw.write_text(screen, f"Attack Power: {current_player.current_attack_power}", font,
                            (cn.map_width * 2 - 1) * cn.tile_width * cn.scale - 50, 10 + 40)


            # Draw tiles
            draw.draw_tiles(screen, map_grid)
            # Draw (highlight) players tiles
            draw.draw_player_tiles(screen, map_grid, players)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:  # Left mouse button clicked
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        if button_rects["Attack"].collidepoint(mouse_x, mouse_y):
                            attack_clicked = not attack_clicked
                            can_extinct = False

                        elif button_rects["Defence"].collidepoint(mouse_x, mouse_y):
                            defense_clicked = not defense_clicked
                            can_extinct = False

                        elif button_rects["Extinct"].collidepoint(mouse_x, mouse_y):
                            # Set the flag to display the confirmation window
                            if can_extinct:
                                confirm_extinction = True

                        elif confirm_extinction:
                            # If confirmation window is displayed, check if "Yes" or "No" button is clicked
                            if yes_button_rect.collidepoint(mouse_x, mouse_y):
                                current_player.extinction()
                                confirm_extinction = False

                            elif no_button_rect.collidepoint(mouse_x, mouse_y):
                                confirm_extinction = False

                        elif button_rects["END TURN"].collidepoint(mouse_x, mouse_y):

                            ss.update_score(current_player)
                            current_player = func.switch_turns(map_grid, current_player)
                            attack_clicked = False
                            can_extinct = True


                        else:
                            # Iterate over the map grid to find the clicked tile
                            for row in range(len(map_grid)):
                                for col in range(len(map_grid[row])):
                                    tile = map_grid[row][col]
                                    center_x, center_y = tile.getX(cn.offset_x, cn.gap), tile.getY(cn.offset_y)
                                    center_x += int(cn.tile_width / 2 * cn.scale)
                                    center_y += int(cn.tile_height // 2 * cn.scale)

                                    # Check if the mouse position is within the bounds of the hexagon
                                    if func.point_in_hexagon(mouse_x, mouse_y, center_x, center_y,
                                                             cn.tile_width * cn.scale,
                                                             cn.tile_height * cn.scale):

                                        if attack_clicked:
                                            func.perform_attack(row, col, map_grid, current_player)

                                        elif defense_clicked:
                                            func.perform_defence(row, col, map_grid, current_player)

                                        break  # Stop checking other tiles if one is already clicked
                                else:
                                    continue
                                break  # Exit outer loop if tile is found


            # Check if attack button is pressed
            if attack_clicked:
                draw.draw_circle_on_tiles(screen, current_player, map_grid, current_player.can_attack)

            # Check if defence button is pressed
            if defense_clicked:
                draw.draw_circle_on_tiles(screen, current_player, map_grid, current_player.tiles)

            # Check if extinction button is pressed
            if confirm_extinction:
                yes_button_rect, no_button_rect = draw.draw_extinction_window(screen)

            # if not current_player.current_civ:
            # print("Fast test to check if player has current spiece")

            pygame.display.flip()



main_loop()
pygame.quit()
