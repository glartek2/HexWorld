import pygame
import pygame.mixer

import random
from collections import deque

import constant as cn
import main_menu
import civilization
import functions as func
import settings
import score_system as ss
import draw_functions as draw


class HexWorld:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("HexWorld")
        self.screen = pygame.display.set_mode((cn.screen_width, cn.screen_height))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.font = pygame.font.Font("resources/fonts/vinque rg.otf", 24)

        self.players = []
        self.current_player = None
        self.civs_queue = deque(self.create_civilizations())

        self.MAIN_MENU, self.SETTINGS, self.GAME, self.END = 0, 1, 2, 3

        self.confirm_extinction = False
        self.force_end_turn = False
        self.attack_clicked = False
        self.defense_clicked = False
        self.can_extinct = True
        self.map_to_create = True
        self.turn_counter = 0
        self.map_grid = None
        self.current_state = self.MAIN_MENU

        self.showing_map = False

    @staticmethod
    def create_civilizations():
        species, abilities = cn.species, cn.abilities
        random.shuffle(abilities)
        random.shuffle(species)

        civilizations = []
        for i in range(len(abilities)):
            civilizations.append(civilization.Civilization(species[i], abilities[i]))

        return civilizations

    def choose_civilization(self):
        available_civs = list(self.civs_queue)[:3]
        selected_civ = None
        running = True

        while running:
            self.screen.fill(cn.BLACK)

            if self.showing_map:
                self.draw_map_only()
                toggle_map_rect = draw.draw_button(self.screen, "Hide Map",
                                                   "resources/buttons/button.png",
                                                   cn.button_x, 400)
            else:
                temp_font = pygame.font.Font("resources/fonts/vinque rg.otf", 64)
                draw.write_text(self.screen, f"Choose Your Civilization: {self.current_player.name}", temp_font,
                                cn.screen_width // 2 - 100, 50)

                button_rects = []
                for idx, civ in enumerate(available_civs):
                    button_rect = draw.draw_button(self.screen, civ.ability.name + " " + civ.species.name,
                                                   f"resources/species/{civ.species.name}.png",
                                                   100 + idx * cn.screen_width // 4, cn.screen_height // 3)
                    button_rects.append((button_rect, civ))

                toggle_map_rect = draw.draw_button(self.screen, "Show Map",
                                                   "resources/buttons/button.png",
                                                   cn.screen_width // 4 + 100,
                                                   cn.screen_height // 2 + cn.button_spacing + cn.button_height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if self.showing_map:
                        if toggle_map_rect.collidepoint(mouse_x, mouse_y):
                            self.showing_map = not self.showing_map
                    else:
                        for button_rect, civ in button_rects:
                            if button_rect.collidepoint(mouse_x, mouse_y):
                                selected_civ = civ
                                running = False
                                break
                        if toggle_map_rect.collidepoint(mouse_x, mouse_y):
                            self.showing_map = not self.showing_map

            pygame.display.flip()

        if selected_civ:
            self.current_player.update_civ(selected_civ)
            self.civs_queue.remove(selected_civ)
            return True
        else:
            return False

    def draw_winner_screen(self, winner):
        self.screen.fill(cn.BLACK)
        temp_font = pygame.font.Font("resources/fonts/vinque rg.otf", 64)
        draw.write_text(self.screen, "Game Over", temp_font, cn.screen_width // 2 - 100, 50)
        winner_text = f"Winner: {winner.name}!"
        draw.write_text(self.screen, winner_text, temp_font, cn.screen_width // 2 - 200, cn.screen_height // 2 - 50)
        pygame.display.flip()

    def get_winner(self):
        return max(self.players, key=lambda player: player.score)

    def draw_map_only(self):
        self.screen.fill(cn.BLACK)
        draw.draw_tiles(self.screen, self.map_grid)
        draw.draw_player_tiles(self.screen, self.map_grid, self.players)

    def initialize_game(self):
        self.map_grid = func.create_map_grid()
        func.fill_map(self.map_grid)

    def draw_game_elements(self):
        self.screen.fill(cn.BLACK)

        button_images = {
            "Attack": "resources/buttons/attack_button.png",
            "Defence": "resources/buttons/defence_button.png",
            "Extinct": "resources/buttons/extinction_button.png" if self.can_extinct
            else "resources/buttons/extinction_button_non_active.png",
            "END TURN": "resources/buttons/end_turn_button.png"
        }

        button_rects = {name: draw.draw_button(self.screen, name, img, pos[0], pos[1])
                        for name, img, pos in
                        zip(button_images.keys(), button_images.values(), cn.button_positions.values())}

        draw.write_text(self.screen, f"Score: {self.current_player.score}", self.font,
                        (cn.map_width * 2 - 1) * cn.tile_width * cn.scale + 100, 20)
        draw.write_text(self.screen, f"Attack Power: {self.current_player.current_attack_power}", self.font,
                        (cn.map_width * 2 - 1) * cn.tile_width * cn.scale + 100, 65)

        draw.draw_tiles(self.screen, self.map_grid)
        draw.draw_player_tiles(self.screen, self.map_grid, self.players)

        return button_rects

    def handle_mouse_click(self, event, button_rects):
        mouse_x, mouse_y = event.pos

        if button_rects["Attack"].collidepoint(mouse_x, mouse_y):
            self.attack_clicked = not self.attack_clicked
            self.can_extinct = False

        elif button_rects["Defence"].collidepoint(mouse_x, mouse_y):
            self.defense_clicked = not self.defense_clicked
            self.can_extinct = False

        elif button_rects["Extinct"].collidepoint(mouse_x, mouse_y):
            if self.can_extinct:
                self.confirm_extinction = True

        elif self.confirm_extinction:
            if self.yes_button_rect.collidepoint(mouse_x, mouse_y):
                self.current_player.extinction()
                self.confirm_extinction = False
                self.can_extinct = False
                self.force_end_turn = True

            elif self.no_button_rect.collidepoint(mouse_x, mouse_y):
                self.confirm_extinction = False

        elif button_rects["END TURN"].collidepoint(mouse_x, mouse_y):
            ss.update_score(self.map_grid, self.current_player)
            self.current_player = func.switch_turns(self.map_grid, self.current_player, self.turn_counter)
            self.attack_clicked = False
            self.can_extinct = True
            self.turn_counter += 1
            self.force_end_turn = False

        else:
            for row in range(len(self.map_grid)):
                for col in range(len(self.map_grid[row])):
                    tile = self.map_grid[row][col]
                    center_x, center_y = tile.get_x(cn.offset_x, cn.gap), tile.get_y(cn.offset_y)
                    center_x += int(cn.tile_width / 2 * cn.scale)
                    center_y += int(cn.tile_height // 2 * cn.scale)

                    if func.point_in_hexagon(mouse_x, mouse_y, center_x, center_y,
                                             cn.tile_width * cn.scale, cn.tile_height * cn.scale):
                        if self.attack_clicked:
                            func.perform_attack(row, col, self.map_grid, self.current_player)
                        elif self.defense_clicked:
                            func.perform_defence(row, col, self.map_grid, self.current_player)
                        return

    def main_loop(self):
        running = True

        while running:
            if self.current_state == self.MAIN_MENU:
                main_menu.main_menu(self.screen)
                self.current_state = self.SETTINGS

            elif self.current_state == self.SETTINGS:
                self.players = settings.settings(self.screen)
                self.current_player = self.players[0]
                for idx, player in enumerate(self.players):
                    player.update_can_attack()
                self.current_state = self.GAME

            elif self.current_state == self.GAME:
                if self.map_to_create:
                    self.initialize_game()
                    self.map_to_create = False

                if not self.current_player.current_civ and not self.force_end_turn:
                    running = self.choose_civilization()

                button_rects = self.draw_game_elements()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_mouse_click(event, button_rects)

                if self.attack_clicked:
                    draw.draw_circle_on_tiles(self.screen, self.current_player, self.map_grid,
                                              self.current_player.can_attack)

                if self.defense_clicked:
                    draw.draw_circle_on_tiles(self.screen, self.current_player, self.map_grid,
                                              self.current_player.tiles)

                if self.confirm_extinction:
                    self.yes_button_rect, self.no_button_rect = draw.draw_extinction_window(self.screen)

                if self.turn_counter >= 10 * settings.num_players:
                    self.current_state = self.END

                pygame.display.flip()


            elif self.current_state == self.END:
                winner = self.get_winner()
                self.draw_winner_screen(winner)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False


        pygame.quit()


if __name__ == "__main__":
    game = HexWorld()
    game.main_loop()
