import pygame as pg
from load_image import load_image

width = 40
height = 40
GRAVITY = 0.35


class Ingridient(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("flower1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def mouse_over(self, mouse):
        return False

    def update(self, platforms):
        self.vy += 0.35
        self.rect = self.rect.move(self.vx, self.vy)

