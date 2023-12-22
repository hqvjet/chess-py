import pygame
from client.tools import get_text_rendered


class Button:
    def __init__(self, x, y, x_step, y_step, width, height, text, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button = pygame.Rect(x, y, width, height)
        self.rendered_text = get_text_rendered(pygame, text,
                                               (x + x_step, y + y_step),
                                               font_size, background=False)
        self.contur = pygame.Rect(x - 3, y - 3, width + 6, height + 6)

    def render(self, screen):
        pygame.draw.rect(screen, (101, 67, 33), self.contur, 5)
        pygame.draw.rect(screen, (255, 255, 255), self.button)
        screen.blit(*self.rendered_text)

    def check_coords(self, coords):
        if coords[0] in range(self.x, self.x + self.width):
            if coords[1] in range(self.y, self.y + self.height):
                return True
        return False