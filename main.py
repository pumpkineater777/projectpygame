import pygame as pg
from ingridient import Ingridient
from load_image import load_image
from object import Object
from porion import Potion

fps = 30

left_win = 100
top_win = 100
win_width = 500
win_height = 500


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + win_width / 2, -t + win_height / 2

    l = min(left_win, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - win_width - left_win), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - win_height - top_win), t)  # Не движемся дальше нижней границы
    t = min(top_win, t)  # Не движемся дальше верхней границы

    return pg.Rect(l, t, w, h)


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


class Map(OnlyImage):
    def recoord(self, x, y):
        self.rect.x = x
        self.rect.y = y


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


class Boarder(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill("grey")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    running = True
    addiction = pg.sprite.Group()
    board = pg.sprite.Group()
    entities = pg.sprite.Group()
    map = Map(0, 0, "potioncraftmap.jpg")
    addiction.add(map)
    board.add(Boarder(0, 0, width, top_win))
    board.add(Boarder(0, left_win, left_win, height - left_win))
    board.add(Boarder(left_win + win_width, top_win, width - (left_win + win_width), height - top_win))
    board.add(Boarder(left_win, top_win + win_height, width - left_win, height - (top_win + win_height)))
    entities.add(OnlyImage(840, 200, "rightobject.png"))
    Bar = bar(988, 222)
    entities.add(Bar)
    platforms = []
    temp = Object(0, 600)
    platforms.append(temp)
    entities.add(temp)
    total_width = 2580
    total_height = 2597
    camera = Camera(camera_configure, total_width, total_height)
    clicked = None
    ingr = []
    INGR = {"letUS.png": 9, "flower1.png": 10}
    inrgidientGroup = pg.sprite.Group()
    temp_x = 4
    temp_y = 4
    hero = Potion(400, 400)
    addiction.add(hero)
    font = pg.font.Font(None, 14)
    direc = [False, False, False, False]
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
    for e in entities:
        screen.blit(e.image, camera.apply(e))
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
                            inrgidientGroup.add(temp)
                            entities.add(temp)
                            clicked = temp
                            my_mouse[1] = event.pos[1] - elem.rect.y
                            my_mouse[0] = event.pos[0] - elem.rect.x
                            INGR[elem.name] -= 1
                            if INGR[elem.name] == 0:
                                INGR.pop(elem.name)
                                elem.kill()
                                ind = ingr.index(elem)
                                ingr.pop(ind)
                        else:
                            clicked = elem
                            my_mouse[1] = event.pos[1] - elem.rect.y
                            my_mouse[0] = event.pos[0] - elem.rect.x
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    direc[0] = True
                if event.key == pg.K_d:
                    direc[1] = True
                if event.key == pg.K_s:
                    direc[2] = True
                if event.key == pg.K_a:
                    direc[3] = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    direc[0] = False
                if event.key == pg.K_d:
                    direc[1] = False
                if event.key == pg.K_s:
                    direc[2] = False
                if event.key == pg.K_a:
                    direc[3] = False
            if event.type == pg.MOUSEBUTTONUP:
                clicked = None
        screen.fill("black")
        hero.update(direc)
        inrgidientGroup.update(platforms)
        if clicked != None:
            mouse_pos = pg.mouse.get_pos()
            clicked.update_mouse(mouse_pos, my_mouse)
        camera.update(hero)
        temp_x = 4
        temp_y = 4
        for e in addiction:
            screen.blit(e.image, camera.apply(e))
        board.draw(screen)
        entities.draw(screen)
        for elem in ingr:
            elem.rect.x = 840 + temp_x
            elem.rect.y = 222 - round(Bar.rect.y - 222) + temp_y
            text = font.render(str(INGR[elem.name]), True, "black")
            text_x = 875 + temp_x
            text_y = 222 + temp_y - round(Bar.rect.y - 222)
            if temp_x == 100:
                temp_x = 4
                temp_y += 48
            else:
                temp_x += 48
            screen.blit(text, (text_x, text_y))
        # сюда надо переставить перерисовку изображения после того как я сделаю изображения прозрачными или до этого цикла поставить прорисовку кликнутого изображения
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
