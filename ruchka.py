import pygame as pg
from load_image import load_image


class Ruchka(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("puchka.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            return True

    def update_mouse(self, mouse, my_mouse):
        mouse_x, mouse_y = mouse
        self.rect.x = mouse_x - my_mouse[0]
        if self.rect.x < 400:
            self.rect.x = 400
        if self.rect.x > 582:
            self.rect.x = 582

