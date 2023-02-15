import pygame as pg
from load_image import load_image


width = 40
height = 40
GRAVITY = 0.35


class Ingridient(pg.sprite.Sprite):
    def __init__(self, x, y, name, group):
        super().__init__()
        self.image = load_image(name)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.on = False
        self.group = group

    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            return True

    def update_mouse(self, mouse, my_mouse):
        mouse_x, mouse_y = mouse
        self.rect.y = mouse_y - my_mouse[1]
        self.rect.x = mouse_x - my_mouse[0]
        self.vy = 0
        self.vx = 0
        self.on = False

    def update(self, platforms):
        if not self.on:
            self.vy += 0.35
        self.rect = self.rect.move(self.vx, self.vy)
        self.collide(platforms)

    def collide(self, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                self.on = True
                self.rect.bottom = p.rect.top
                self.vy = 0

    def set_coords(self,x, y):
        self.rect.x = x
        self.rect.y = y

