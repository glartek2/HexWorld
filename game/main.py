import pygame
import pygame.mixer

import constant as cn
import main_menu
import civilization
import spieces
import ability
import functions as func
import settings
import score_system as ss
import draw_functions as draw


class HexagonalMapGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hexagonal Map")
        self.screen = pygame.display.set_mode((cn.screen_width, cn.screen_height))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.font = pygame.font.Font("resources/fonts/vinque rg.otf", 24)

        self.players = []
        self.current_player = None
        self.civs = self.create_test_civilizations()

        self.confirm_extinction = False
        self.attack_clicked = False
        self.defense_clicked = False
        self.can_extinct = True
        self.map_to_create = True
        self.turn_counter = 0
        self.map_grid = None
        self.current_state = 0

        self.MAIN_MENU, self.SETTINGS, self.GAME, self.END = 0, 1, 2, 3

    @staticmethod
    def create_test_civilizations():
        return [
            civilization.Civilization(spieces.Spieces("Dwarves", 4), ability.Ability("Flying", 4)),
            civilization.Civilization(spieces.Spieces("Trytons", 7), ability.Ability("Dino Tamers", 4)),
            civilization.Civilization(spieces.Spieces("Simple", 7), ability.Ability(None, 4)),
            civilization.Civilization(spieces.Spieces("Simple", 7), ability.Ability(None, 4)),
        ]

    def initialize_game(self):
        self.map_grid = func.create_map_grid()
        func.fill_map(self.map_grid)

    def draw_game_elements(self):
        self.screen.fill(cn.BLACK)

        button_images = {
            "Attack": "resources/buttons/attack_button.png",
            "Defence": "resources/buttons/defence_button.png",
            "Extinct": "resources/buttons/extinction_button.png" if self.can_extinct else "resources/buttons/extinction_button_non_active.png",
            "END TURN": "resources/buttons/end_turn_button.png"
        }

        button_rects = {name: draw.draw_button(self.screen, name, img, pos[0], pos[1])
                        for name, img, pos in
                        zip(button_images.keys(), button_images.values(), cn.button_positions.values())}

        draw.write_text(self.screen, f"Score: {self.current_player.score}", self.font,
                        (cn.map_width * 2 - 1) * cn.tile_width * cn.scale - 50, 10)
        draw.write_text(self.screen, f"Attack Power: {self.current_player.current_attack_power}", self.font,
                        (cn.map_width * 2 - 1) * cn.tile_width * cn.scale - 50, 50)

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

            elif self.no_button_rect.collidepoint(mouse_x, mouse_y):
                self.confirm_extinction = False

        elif button_rects["END TURN"].collidepoint(mouse_x, mouse_y):
            ss.update_score(self.map_grid, self.current_player)
            self.current_player = func.switch_turns(self.map_grid, self.current_player, self.turn_counter)
            self.attack_clicked = False
            self.can_extinct = True
            self.turn_counter += 1

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
                    player.update_civ(self.civs[idx])
                    player.update_tiles((idx, idx))
                    player.update_can_attack()
                self.current_state = self.GAME

            elif self.current_state == self.GAME:
                if self.map_to_create:
                    self.initialize_game()
                    self.map_to_create = False

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

        pygame.quit()


if __name__ == "__main__":
    game = HexagonalMapGame()
    game.main_loop()
