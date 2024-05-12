import pygame
import sys
from draw_functions import draw_button
from constant import WHITE, BLACK, screen_width, button_width, screen_height


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def lerp_color(color1, color2, alpha):
    r = int(color1[0] * (1 - alpha) + color2[0] * alpha)
    g = int(color1[1] * (1 - alpha) + color2[1] * alpha)
    b = int(color1[2] * (1 - alpha) + color2[2] * alpha)
    return (r, g, b)



# Function to display main menu
def main_menu(screen):
    screen.fill(BLACK)
    start_color = (30, 87, 153)  # Example start color
    end_color = (76, 163, 224)  # Example end color

    # Animation parameters
    anim_speed = 0.02  # Adjust animation speed
    alpha = 0


    while True:

        # Calculate interpolated color based on alpha
        current_color = lerp_color(start_color, end_color, alpha)

        # Fill the screen with the interpolated color
        screen.fill(current_color)

        # Update alpha for smooth animation
        alpha += anim_speed
        if alpha >= 1 or alpha <= 0:
            anim_speed = -anim_speed  # Reset alpha after reaching 1

        # Load image
        image = pygame.image.load("resources/main_menu/Main_menu_image.png")

        # Draw image on button surface
        button_image_rect = image.get_rect()
        button_image_rect.x -= image.get_size()[0] // 6
        button_image_rect.y += 20
        screen.blit(image, button_image_rect)

        # Draw title
        title_font = pygame.font.Font("resources/fonts/vinque rg.otf", 64)
        draw_text("HexWorld", title_font, WHITE, screen, screen_width // 2, screen_height // 4)

        # Draw "Play" button
        play_button_rect = draw_button(screen, "Play", "resources/buttons/button.png",
                                       screen_width // 2 - button_width // 2, screen_height // 2)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_x, mouse_y):
                    return  # Go to the game (return)


        pygame.time.Clock().tick(60)
        pygame.display.flip()
