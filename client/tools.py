import os
import sys

import requests

import client.parameters as para


def get_text_rendered(pygame, text, coords, size, is_center=False,
                      background=True, italic=False):
    font = pygame.font.Font(None, size)
    font.set_italic(italic)
    if background:
        text_rendered = font.render(text, 1, (194, 107, 16), (255, 255, 255))
    else:
        text_rendered = font.render(text, 1, (194, 107, 16))
    text_rect = text_rendered.get_rect()
    text_rect.top = coords[1]
    if is_center:
        text_rect.x = (para.WIDTH - text_rect.width) // 2
    else:
        text_rect.x = coords[0]
    return text_rendered, text_rect


def terminate(pygame, player_key):
    if player_key is not None:
        try:
            requests.get(para.SERVER_ADDRESS + 'close_session/{}'.format(player_key))
        except Exception:
            pass
    pygame.quit()
    sys.exit()


def load_image(pygame, name, colorkey=None):
    fullname = os.path.join('res/pictures/', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
