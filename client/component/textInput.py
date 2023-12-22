import pygame

from client.tools import get_text_rendered


class TextInput:
    def __init__(self, x, y, width, height, font_size, max_len, hide=False):
        self.is_selected = False
        self.x = x
        self.y = y
        self.text = ''
        self.width = width
        self.height = height
        self.font_size = font_size
        self.hide = hide
        self.rendered_text = get_text_rendered(pygame, self.text, (x, y),
                                               font_size, background=True)
        self.line = pygame.Rect(self.x, self.y + self.height, self.width, 2)
        self.contur = pygame.Rect(x - 3, y - 3, width + 6, height + 6)
        self.max_len = max_len

    def render(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, (101, 67, 33), self.contur)
        pygame.draw.rect(screen, (101, 67, 33), self.line)
        screen.blit(*self.rendered_text)

    def update(self, key):
        if self.is_selected:
            try:
                char = key.unicode
                if char.isalnum():
                    if self.max_len > len(self.text):
                        self.text += char
                else:
                    if ord(char) == 8:
                        if len(self.text) > 0:
                            self.text = self.text[:-1]
            except Exception:
                pass
        if self.hide:
            self.rendered_text = get_text_rendered(pygame, '*' * len(self.text),
                                                   (self.x, self.y),
                                                   self.font_size,
                                                   background=True)
        else:
            self.rendered_text = get_text_rendered(pygame, self.text,
                                                   (self.x, self.y),
                                                   self.font_size,
                                                   background=True)

    def check_coords(self, coords):
        if coords[0] in range(self.x, self.x + self.width):
            if coords[1] in range(self.y, self.y + self.height):
                self.is_selected = True
            else:
                self.is_selected = False
        else:
            self.is_selected = False

    def clear(self):
        self.text = ''
        self.rendered_text = get_text_rendered(pygame, '',
                                               (self.x, self.y),
                                               self.font_size,
                                               background=True)

    def get_text(self):
        return self.text
