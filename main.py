import pygame as pg
from ingridient import Ingridient
from load_image import load_image
from object import Object

fps = 30


class OnlyImage(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.image = load_image(name)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def mouse_over(self, mouse):
        return False


class Inridient_photo(OnlyImage):
    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


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

    def update_mouse(self, mouse, my_mouse):
        mouse_x, mouse_y = mouse
        self.rect.y = mouse_y - my_mouse[1]
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
    entities.add(OnlyImage(840, 200, "rightobject.png"))
    Bar = bar(988, 222)
    entities.add(Bar)
    platforms = []
    temp = Object(0, 600)
    platforms.append(temp)
    entities.add(temp)
    clicked = None
    ingr = []
    INGR = {"letUS.png": 9, "flower1.png": 10}
    temp_x = 4
    temp_y = 4
    font = pg.font.Font(None, 14)
    for elem in INGR:
        temp = Inridient_photo(840 + temp_x, 222 + temp_y, elem)
        entities.add(temp)
        text = font.render(str(INGR[elem]), True, "black")
        text_x = 875 + temp_x
        text_y = 222 + temp_y - (Bar.rect.y - 222)
        ingr.append(temp)
        if temp_x == 100:
            temp_x = 0
            temp_y += 48
        else:
            temp_x += 48
        screen.blit(text, (text_x, text_y))
    entities.draw(screen)
    pg.display.flip()
    my_mouse = [0, 0]
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in entities:
                    if elem.mouse_over(event.pos):
                        if elem == Bar:
                            clicked = elem
                            my_mouse[1] = event.pos[1] - elem.rect.y
                            my_mouse[0] = event.pos[0] - elem.rect.x
                        elif elem in ingr:
                            temp = Ingridient(elem.rect.y, elem.rect.x, elem.name)
                            entities.add(temp)
                            clicked = temp
                            my_mouse[1] = event.pos[1] - elem.rect.y
                            my_mouse[0] = event.pos[0] - elem.rect.x
                            INGR[elem.name] -= 1
                            if INGR[elem.name] == 0:
                                INGR.pop(elem.name)
                                elem.kill()
                                print(INGR)
                                ind = ingr.index(elem)
                                ingr.pop(ind)
                        else:
                            clicked = elem
                            my_mouse[1] = event.pos[1] - elem.rect.y
                            my_mouse[0] = event.pos[0] - elem.rect.x
            if event.type == pg.MOUSEBUTTONUP:
                clicked = None
        screen.fill("black")
        entities.update(platforms)
        if clicked != None:
            mouse_pos = pg.mouse.get_pos()
            clicked.update_mouse(mouse_pos, my_mouse)
        temp_x = 4
        temp_y = 4
        entities.draw(screen)
        print(ingr)
        for elem in ingr:
            elem.rect.x = 840 + temp_x
            elem.rect.y = 222 - (Bar.rect.y - 222) + temp_y
            text = font.render(str(INGR[elem.name]), True, "black")
            text_x = 875 + temp_x
            text_y = 222 + temp_y - (Bar.rect.y - 222)
            if temp_x == 100:
                temp_x = 4
                temp_y += 48
            else:
                temp_x += 48
            screen.blit(text, (text_x, text_y))
        print(ingr)
        # сюда надо переставить перерисовку изображения после того как я сделаю изображения прозрачными или до этого цикла поставить прорисовку кликнутого изображения
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
