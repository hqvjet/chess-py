import random
import pygame as pg
import client.parameters as para

from client.tools import load_image


class Particle(pg.sprite.Sprite):

    def __init__(self, pygame, pos, dx, dy):
        super().__init__(para.sprites_star)
        fire = [load_image(pygame, "star.png")]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        self.image = random.choice(fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(para.screen_rect):
            self.kill()
