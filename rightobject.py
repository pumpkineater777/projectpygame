import pygame as pg


class RightThing(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((200, 500))
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
