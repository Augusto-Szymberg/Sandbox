import pygame
from config import LIGHT_GREY

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        # Draw the button rectangle
        pygame.draw.rect(surface, LIGHT_GREY, self.rect)
        # Draw the button text
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class ParticleSelectionButton:
    def __init__(self, x, y, size, image, particle_id):
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = pygame.Rect(x, y, size, size)
        self.particle_id = particle_id

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, position):
        return self.rect.collidepoint(position)

class ParticleSelectionIndicator:
    def __init__(self, x, y, width, height, image, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_font_size = 36  # Larger font size for the text below the image
        self.image = pygame.transform.scale(image, (width, height))  # Resize image to fit
        self.text = text

    def draw(self, surface):
        # Draw the resized image
        surface.blit(self.image, self.rect)

        # Draw the text below the image
        font = pygame.font.Font(None, self.text_font_size)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.y + self.rect.height + text_surf.get_height() // 2))
        surface.blit(text_surf, text_rect)

    def set_image(self, new_image):
        # Resize the new image
        self.image = pygame.transform.scale(new_image, (self.rect.width, self.rect.height))

    def set_text(self, new_text):
        self.text = new_text

