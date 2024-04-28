import pygame
from constant import button_height, button_width, BLACK


# Function to draw buttons with text and image
def draw_button(screen, text, image_path, x, y):
    font = pygame.font.Font("resources/fonts/VTCGoblinHand.ttf", 28)
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