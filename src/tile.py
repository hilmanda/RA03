import pygame
from src.menu import *
from src.music import *
from src.start import *
from src.game import *
class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('assets/cards/' + filename)

        self.back_image = pygame.image.load('assets/back.jpg')
        # pygame.draw.rect(self.back_image, self.back_image, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False