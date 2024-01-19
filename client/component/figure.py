from client.tools import load_image
import client.parameters as para
import pygame as pg

figure_images = {}


def init_figure_images(pygame):
    global figure_images
    figure_images = {'bB': load_image(pygame, 'bB.png'),
                     'bK': load_image(pygame, 'bK.png'),
                     'bN': load_image(pygame, 'bN.png'),
                     'bP': load_image(pygame, 'bP.png'),
                     'bQ': load_image(pygame, 'bQ.png'),
                     'bR': load_image(pygame, 'bR.png'),
                     'wB': load_image(pygame, 'wB.png'),
                     'wK': load_image(pygame, 'wK.png'),
                     'wN': load_image(pygame, 'wN.png'),
                     'wP': load_image(pygame, 'wP.png'),
                     'wQ': load_image(pygame, 'wQ.png'),
                     'wR': load_image(pygame, 'wR.png')}


class Figure(pg.sprite.Sprite):
    def __init__(self, figure_type, pos_x, pos_y, group):
        super().__init__(group)
        self.x = pos_x
        self.y = pos_y
        print(figure_type)
        self.image = figure_images[figure_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(para.FIGURE_WIDTH * pos_x + 20 * pos_x + 10,
                                   para.FIGURE_HEIGHT * pos_y + 20 * pos_y + 10)

    def update_coords(self, new_coords):
        pos_x = new_coords[0]
        pos_y = new_coords[1]
        self.x = new_coords[0]
        self.y = new_coords[1]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(para.FIGURE_WIDTH * pos_x + 20 * pos_x + 10,
                                   para.FIGURE_HEIGHT * pos_y + 20 * pos_y + 10)

    def get_coords(self):
        return self.x, self.y
