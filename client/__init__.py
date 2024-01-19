import pygame
import client.parameters as para

from client.ui import start_screen
from client.ui.findOpponent import start_finding_opponent
from client.ui.login import login_screen
from client.ui.offlineMode import select_diff

pygame.init()
pygame.mixer.music.load('res/music/background.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(para.SIZE)
para.figures_sprites = pygame.sprite.Group()
para.sprites_star = pygame.sprite.Group()

while(True):
    if para.BACK_TO == 'start_screen':
        start_screen(pygame, screen, clock)
        para.BACK_TO = ''
        # Offline
        if para.GAMEMODE == 0:
            select_diff(pygame, screen, clock)
        # Online
        else:
            login_screen(pygame, screen, clock)
            if para.BACK_TO != '':
                continue
            start_finding_opponent(pygame, screen, clock)
