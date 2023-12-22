import pygame
import client.parameters as para

from client.ui import start_screen
from client.ui.findOpponent import start_finding_opponent
from client.ui.login import login_screen

pygame.init()
pygame.mixer.music.load('res/music/background.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(para.SIZE)
para.figures_sprites = pygame.sprite.Group()
para.sprites_star = pygame.sprite.Group()

start_screen(pygame, screen, clock)

#Offline
if para.GAMEMODE == 0:
    pass
#Online
else:
    login_screen(pygame, screen, clock)
    start_finding_opponent(pygame, screen, clock)
