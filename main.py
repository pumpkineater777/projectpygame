import pygame as pg
from ingridient import Ingridient
from load_image import load_image
from object import Object

fps = 30


class OnlyImage(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def mouse_over(self, mouse):
        return False


class bar(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((10, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            return True

    def update_mouse(self, mouse, ots):
        mouse_x, mouse_y = mouse
        self.rect.y = mouse_y - ots
        if self.rect.y < 222:
            self.rect.y = 222
        if self.rect.y > 582 - 60:
            self.rect.y = 582 - 60


if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    running = True
    entities = pg.sprite.Group()
    entities.add(Ingridient(40, 40))
    entities.add(OnlyImage(840, 200, "rightobject.png"))
    Bar = bar(988, 222)
    entities.add(Bar)
    platforms = []
    temp = Object(0, 600)
    platforms.append(temp)
    entities.add(temp)
    clicked = None
    ingr = []
    INGR = [("flower1.png", 9), ("flower1.png", 10), ("flower1.png", 9), ("flower1.png", 10)]
    temp_x = 4
    temp_y = 4
    for elem in INGR:
        print(1)
        temp = OnlyImage(840 + temp_x, 222 + temp_y, elem[0])
        ingr.append(temp)
        entities.add(temp)
        if temp_x == 100:
            temp_x = 0
            temp_y += 48
        else:
            temp_x += 48
    entities.draw(screen)
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in entities:
                    if elem.mouse_over(event.pos):
                        clicked = elem
                        mouse_y = event.pos[1] - elem.rect.y
            if event.type == pg.MOUSEBUTTONUP:
                clicked = None
        screen.fill("black")
        entities.update(platforms)
        if clicked != None:
            mouse_pos = pg.mouse.get_pos()
            clicked.update_mouse(mouse_pos, mouse_y)
        temp_x = 4
        temp_y = 4
        for elem in ingr:
            elem.rect.y = 222 - (Bar.rect.y - 222) + temp_y
            elem.rect.x = 840 + temp_x
            if temp_x == 100:
                temp_x = 0
                temp_y += 48
            else:
                temp_x += 48
        entities.draw(screen)
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
