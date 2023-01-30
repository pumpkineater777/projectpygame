import pygame as pg
from load_image import load_image

move_speed = 7


class Potion(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("potionlazy.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.direc = [0, 0]

    def update(self, direc):
        self.vy = 0
        self.vx = 0
        if direc[0]:
            self.vy = -move_speed
        if direc[1]:
            self.vx = move_speed
        if direc[2]:
            self.vy = move_speed
        if direc[3]:
            self.vx = -move_speed
        if self.direc[0] < 0 and direc[0]:
            self.vy = -move_speed
        if self.direc[0] > 0 and direc[2]:
            self.vy = move_speed
        if self.direc[1] < 0 and direc[3]:
            self.vx = -move_speed
        if self.direc[1] > 0 and direc[1]:
            self.vx = move_speed
        self.rect = self.rect.move(self.vx, self.vy)
        if self.vy > 0:
            self.direc[0] = 1
        elif self.vy < 0:
            self.direc[0] = -1
        else:
            self.direc[0] = 0
        if self.vx > 0:
            self.direc[1] = 1
        elif self.vx < 0:
            self.direc[1] = -1
        else:
            self.direc[1] = 0

    def mouse_over(self, mouse):
        return False

    def set_coords(self, x, y):
        self.rect.x += x
        self.rect.y += y
