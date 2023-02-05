import pygame as pg
from ingridient import Ingridient
from load_image import load_image
from object import Object
from porion import Potion
from bpwl import Bowl
from ruchka import Ruchka
from sellings import customer

fps = 60

left_win = 50
top_win = 50
win_width = 600
win_height = 400
Path = [
    (1.1422428770797097, 2.774036987814088), (1.1422428770797097, 2.774036987814089),
    (1.1422428770797097, 2.774036987814089), (1.1422428770797097, 2.774036987814089),
    (1.1422428770797097, 2.774036987814089), (1.1422428770797097, 2.774036987814089),
    (1.1422428770797097, 2.774036987814089), (1.1422428770797097, 2.774036987814089),
    (1.1422428770797097, 2.774036987814089), (1.1422428770797097, 2.7740369878140854),
    (1.1422428770797097, 2.7740369878140854), (1.1422428770797097, 2.7740369878140854),
    (1.1422428770797097, 2.7740369878140854), (0.26563982260866936, 2.988216104073537),
    (0.26563982260866936, 2.988216104073537), (0.26563982260866226, 2.988216104073537),
    (0.26563982260866226, 2.988216104073537), (0.26563982260866226, 2.988216104073537),
    (0.26563982260866226, 2.988216104073537), (0.26563982260866226, 2.988216104073537),
    (0.26563982260866226, 2.988216104073537), (0.26563982260866226, 2.988216104073544),
    (0.26563982260866226, 2.988216104073544), (0.26563982260866226, 2.988216104073544),
    (0.26563982260866226, 2.988216104073544), (0.26563982260866226, 2.988216104073544),
    (0.26563982260866226, 2.988216104073544), (0.26563982260866226, 2.988216104073544),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-0.5883518724062071, 2.9417413336723115), (-0.5883518724062071, 2.9417413336723115),
    (-1.9295658644662481, 2.2971233259637245), (-1.9295658644662481, 2.2971233259637245),
    (-1.9295658644662481, 2.2971233259637245), (-1.9295658644662446, 2.2971233259637245),
    (-1.9295658644662446, 2.2971233259637245), (-1.9295658644662446, 2.2971233259637245),
    (-1.9295658644662446, 2.2971233259637245), (-1.9295658644662446, 2.2971233259637245),
    (-1.9295658644662446, 2.2971233259637245), (-1.9295658644662446, 2.2971233259637245),
    (-1.9295658644662446, 2.2971233259637245), (-2.5827589906068305, 1.5262227872887877),
    (-2.5827589906068287, 1.5262227872887877), (-2.5827589906068287, 1.5262227872887877),
    (-2.5827589906068287, 1.5262227872887877), (-2.5827589906068287, 1.5262227872887877),
    (-2.582758990606829, 1.5262227872887877), (-2.582758990606829, 1.5262227872887877),
    (-2.582758990606829, 1.5262227872887877), (-2.582758990606829, 1.5262227872887877),
    (-1.0535642096411397, 2.8089148182462225), (-1.0535642096411397, 2.8089148182462225),
    (-1.0535642096411397, 2.8089148182462225), (-1.0535642096411397, 2.8089148182462225),
    (-1.0535642096411397, 2.8089148182462225), (-1.0535642096411397, 2.8089148182462225),
    (-1.0535642096411397, 2.8089148182462225), (-1.0535642096411397, 2.8089148182462225),
    (-1.0535642096411397, 2.8089148182462225), (-1.0535642096411397, 2.8089148182462225),
    (-1.0535642096411397, 2.8089148182462225), (-1.0535642096411397, 2.8089148182462225),
    (-0.14968707048212382, 2.9962633030043264), (-0.14968707048212382, 2.996263303004355),
    (-0.14968707048212382, 2.996263303004355), (-0.14968707048212382, 2.996263303004355),
    (-0.14968707048212382, 2.996263303004355), (-0.14968707048212382, 2.996263303004355),
    (-0.14968707048212382, 2.996263303004355), (-0.14968707048212382, 2.996263303004355),
    (-0.14968707048212382, 2.996263303004355), (-0.14968707048212382, 2.996263303004355),
    (-0.14968707048212393, 2.996263303004355), (-0.14968707048212393, 2.996263303004355),
    (-0.14968707048212393, 2.996263303004355), (-0.14968707048212393, 2.996263303004355),
    (-0.14968707048212393, 2.996263303004355), (-0.14968707048212393, 2.996263303004355),
    (-0.14968707048212393, 2.996263303004355), (-0.14968707048212393, 2.996263303004355),
    (-0.14968707048212393, 2.996263303004355), (-0.14968707048212393, 2.996263303004355),
    (-0.14968707048212393, 2.996263303004355), (0.8620815595491362, 2.8734674845359507),
    (0.8620815595491367, 2.8734674845359223), (0.8620815595491367, 2.8734674845359223),
    (0.8620815595491367, 2.8734674845359223), (0.8620815595491367, 2.8734674845359223),
    (0.8620815595491367, 2.8734674845359223), (0.8620815595491358, 2.8734674845359223),
    (0.8620815595491358, 2.8734674845359223), (0.8620815595491358, 2.8734674845359223),
    (0.8620815595491358, 2.8734674845359223), (0.8620815595491358, 2.8734674845359223),
    (0.8620815595491358, 2.8734674845359223), (0.8620815595491358, 2.8734674845359223),
    (0.8620815595491358, 2.8734674845359223), (2.415302671749208, 1.7794136685552076),
    (2.415302671749206, 1.7794136685552076), (2.415302671749206, 1.7794136685552076),
    (2.415302671749206, 1.7794136685552076), (2.415302671749206, 1.7794136685552076),
    (2.415302671749206, 1.7794136685552076), (2.415302671749206, 1.7794136685552076),
    (2.4153026717492025, 1.7794136685552076), ]
poor_dict = {0: ("ingidient_", 840), 1: ("potion_", 927)}
poor_mass_dict = {0: ("taverna_", 0), 1: ("laborat_", 50)}
INGR = {"letUS.png": 9, "flower1.png": 10}
POTIONS = {"potion_photo.png": 2}


class Only_rect(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(color)

    def recolor(self, color):
        self.image.fill(color)

    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


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
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.mask = pg.mask.from_surface(self.image)

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


class EndPoint(OnlyImage):
    def __init__(self, x, y, name, potion):
        super().__init__(x, y, name)
        self.mask = pg.mask.from_surface(self.image)
        self.potion = potion


if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    running = True
    entities_taverna = pg.sprite.Group()
    entities_taverna.add(OnlyImage(0, 0, "background.png"))
    direc_taverna = [-1, -1]
    cust = customer(800, 400)
    entities_taverna.add(cust)
    entities_taverna.draw(screen)
    addiction = pg.sprite.Group()
    board = pg.sprite.Group()
    entities = pg.sprite.Group()
    map = Map(0, 0, "potioncraftmap.jpg")
    kill_map = Map(415, 250, "mapkill.png")
    addiction.add(kill_map)
    addiction.add(map)
    board.add(Boarder(0, 0, width, top_win))
    board.add(Boarder(0, left_win, left_win, height - left_win))
    board.add(Boarder(left_win + win_width, top_win, width - (left_win + win_width), height - top_win))
    board.add(Boarder(left_win, top_win + win_height, width - left_win, height - (top_win + win_height)))
    individ_board = pg.sprite.Group()
    individ_board.add(Boarder(840, 0, 160, 200))
    entities.add(OnlyImage(400, 417, "chunk.png"))
    entities.add(OnlyImage(840, 200, "rightobject.png"))
    ruchka = Ruchka(430, 355)
    entities.add(ruchka)
    temp = Bowl(430, 420)
    entities.add(temp)
    kills = [temp]
    Bar = bar(988, 222)
    entities.add(Bar)
    platforms = []
    temp = Object(0, 650)
    platforms.append(temp)
    entities.add(temp)
    total_width = 2580
    total_height = 2597
    camera = Camera(camera_configure, total_width, total_height)
    clicked = None
    ingr = []
    moveGroup = pg.sprite.Group()
    temp_x = 4
    temp_y = 4
    hero = Potion(1284, 1284)
    addiction.add(hero)
    could_potion_and = False
    rectangle = Only_rect(50, 530, 280, 70, "blue")
    entities.add(rectangle)
    font = pg.font.Font(None, 14)
    direc = [False, False, False, False]
    pointed = [None, None]
    big_path = []
    end_point = []
    temp = EndPoint(1200, 1200, "potionlazy.png", "potion_photo.png")
    end_point.append(temp)
    addiction.add(temp)
    discard_button = Inridient_photo(75, 465, "discard.png")
    entities.add(discard_button)
    font_end = pg.font.Font(None, 40)
    text_end = font_end.render("Завершить зелье", True, "black")
    screen.blit(text_end, (100, 600))
    mass_butt = []
    act_mass_butt = 1
    mass_butt_group = pg.sprite.Group()
    temp = Inridient_photo(poor_mass_dict[0][1], 0, "taverna_passive.png")
    mass_butt.append(temp)
    mass_butt_group.add(temp)
    temp = Inridient_photo(poor_mass_dict[1][1], 0, "laborat_active.png")
    mass_butt.append(temp)
    mass_butt_group.add(temp)
    buttons = []
    active_button = 0
    buttons_group = pg.sprite.Group()
    temp = Inridient_photo(poor_dict[0][1], 100, "ingidient_active.png")
    buttons.append(temp)
    buttons_group.add(temp)
    buttons_group.draw(screen)
    temp = Inridient_photo(poor_dict[1][1], 100, "potion_passive.png")
    buttons.append(temp)
    buttons_group.add(temp)
    ingr_photo = pg.sprite.Group()
    for elem in INGR:
        temp = Inridient_photo(840 + temp_x, 222 + temp_y, elem)
        ingr_photo.add(temp)
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
    poti = []
    poti_photo = pg.sprite.Group()
    temp_x = 4
    temp_y = 4
    for elem in POTIONS:
        temp = Inridient_photo(840 + temp_x, 222 + temp_y, elem)
        poti_photo.add(temp)
        text = font.render(str(POTIONS[elem]), True, "black")
        text_x = 875 + temp_x
        text_y = 222 + temp_y - (Bar.rect.y - 222)
        poti.append(temp)
        if temp_x == 100:
            temp_x = 0
            temp_y += 48
        else:
            temp_x += 48
        screen.blit(text, (text_x, text_y))
    for e in addiction:
        screen.blit(e.image, camera.apply(e))
    entities.draw(screen)
    individ_board.draw(screen)
    pg.display.flip()
    my_mouse = [0, 0]
    timer = 0
    tempopary = pg.sprite.Group()
    path = []
    index = 0
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                if act_mass_butt == 1:
                    for elem in *entities, *ingr_photo, *poti_photo:
                        if elem.mouse_over(event.pos) and event.pos[1] >= 200:
                            if (elem in ingr and active_button == 0) or (elem in poti and active_button == 1):
                                pointed = pointed[1], elem
                                break
                    else:
                        pointed = pointed[1], None
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in *entities, *moveGroup, *buttons_group, *ingr_photo, *poti_photo, *mass_butt_group:
                    if elem.mouse_over(event.pos):
                        if elem in mass_butt:
                            if mass_butt.index(elem) != act_mass_butt:
                                mass_butt[act_mass_butt].kill()
                                mass_butt[act_mass_butt] = Inridient_photo(poor_mass_dict[act_mass_butt][1], 0,
                                                                           poor_mass_dict[act_mass_butt][
                                                                               0] + "passive.png")
                                mass_butt_group.add(mass_butt[act_mass_butt])
                                act_mass_butt = mass_butt.index(elem)
                                mass_butt[act_mass_butt].kill()
                                mass_butt[act_mass_butt] = Inridient_photo(poor_mass_dict[act_mass_butt][1], 0,
                                                                           poor_mass_dict[act_mass_butt][
                                                                               0] + "active.png")
                                mass_butt_group.add(mass_butt[act_mass_butt])
                        elif act_mass_butt == 1:
                            if elem in buttons:
                                if buttons.index(elem) != active_button:
                                    buttons[active_button].kill()
                                    buttons[active_button] = Inridient_photo(poor_dict[active_button][1], 100,
                                                                             poor_dict[active_button][
                                                                                 0] + "passive.png")
                                    buttons_group.add(buttons[active_button])
                                    active_button = buttons.index(elem)
                                    buttons[active_button].kill()
                                    buttons[active_button] = Inridient_photo(poor_dict[active_button][1], 100,
                                                                             poor_dict[active_button][0] + "active.png")
                                    buttons_group.add(buttons[active_button])
                            elif elem in ingr:
                                if event.pos[1] >= 200 and active_button == 0:
                                    temp = Ingridient(elem.rect.y, elem.rect.x, elem.name, "ingr")
                                    moveGroup.add(temp)
                                    clicked = temp
                                    my_mouse[1] = event.pos[1] - elem.rect.y
                                    my_mouse[0] = event.pos[0] - elem.rect.x
                                    INGR[elem.name] -= 1
                                    if INGR[elem.name] == 0:
                                        INGR.pop(elem.name)
                                        elem.kill()
                                        ind = ingr.index(elem)
                                        ingr.pop(ind)
                            elif elem in poti:
                                if event.pos[1] >= 200 and active_button == 1:
                                    temp = Ingridient(elem.rect.y, elem.rect.x, elem.name, "poti")
                                    moveGroup.add(temp)
                                    clicked = temp
                                    my_mouse[1] = event.pos[1] - elem.rect.y
                                    my_mouse[0] = event.pos[0] - elem.rect.x
                                    POTIONS[elem.name] -= 1
                                    if POTIONS[elem.name] == 0:
                                        POTIONS.pop(elem.name)
                                        elem.kill()
                                        ind = poti.index(elem)
                                        poti.pop(ind)
                            elif elem == rectangle:
                                if could_potion_and:
                                    hero.set_coords(1284, 1284)
                                    if could_potion_and.potion in POTIONS:
                                        POTIONS[could_potion_and.potion] += 1
                                    else:
                                        POTIONS[could_potion_and.potion] = 1
                                    for elem in big_path:
                                        elem.kill()
                                    big_path = []
                                    path = []
                                    could_potion_and = False
                                    index = 0
                            elif elem == discard_button:
                                hero.set_coords(1284, 1284)
                                for elem in big_path:
                                    elem.kill()
                                big_path = []
                                path = []
                                index = 0
                            else:
                                clicked = elem
                                my_mouse[1] = event.pos[1] - elem.rect.y
                                my_mouse[0] = event.pos[0] - elem.rect.x
            if event.type == pg.KEYDOWN:
                if act_mass_butt == 1:
                    if event.key == pg.K_w:
                        direc[0] = True
                    if event.key == pg.K_d:
                        direc[1] = True
                    if event.key == pg.K_s:
                        direc[2] = True
                    if event.key == pg.K_a:
                        direc[3] = True
                else:
                    if event.key == pg.K_SPACE:
                        if direc_taverna[0] == -1:
                            direc_taverna[0] = (direc_taverna[1] + 1) % 2
                            direc_taverna[1] = direc_taverna[0]
            if event.type == pg.KEYUP:
                if act_mass_butt == 1:
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
        if act_mass_butt == 1:
            if pointed[0] == pointed[1] != None:
                timer += 1
            else:
                timer = 0
                for elem in tempopary:
                    elem.kill()
            if timer >= 50:
                if pointed[0] in ingr or pointed[0] in poti:
                    temp = OnlyImage(pointed[0].rect.x - 75, pointed[0].rect.y + 50, "amistupid.jpg")
                    tempopary.add(temp)
                    entities.add(temp)
            hero.update(direc)
            if pg.sprite.collide_mask(hero, kill_map):
                hero.set_coords(1284, 1284)
                path = []
                for elem in big_path:
                    elem.kill()
                big_path = []
                index = 0
            moveGroup.update(platforms)
            for self in moveGroup:
                for k in kills:
                    if pg.sprite.collide_rect(self, k):
                        if self != clicked and self.group == "ingr":
                            self.kill()
                            temp = OnlyImage(hero.rect.x - 30, hero.rect.y + 10, "path.png")
                            addiction.add(temp)
                            path.append(Path)
                            big_path.append(temp)
            camera.update(hero)
            if clicked == ruchka:
                mouse_pos = pg.mouse.get_pos()
                temp = ruchka.rect.x
                clicked.update_mouse(mouse_pos, my_mouse)
                if ruchka.rect.x - temp != 0:
                    for i in range(len(path)):
                        if index >= len(path[0]):
                            index -= len(path[0])
                            path.pop(0)
                            big_path.pop(0).kill()
                        else:
                            hero.move_coords(path[0][index][0], path[0][index][1])
                            index += 1
            elif clicked != None:
                mouse_pos = pg.mouse.get_pos()
                clicked.update_mouse(mouse_pos, my_mouse)
            temp_x = 4
            temp_y = 4
            for e in addiction:
                screen.blit(e.image, camera.apply(e))
            board.draw(screen)
            entities.draw(screen)
            if active_button == 0:
                ingr_photo.draw(screen)
            else:
                poti_photo.draw(screen)
            for elem in end_point:
                if pg.sprite.collide_mask(hero, elem):
                    could_potion_and = elem
                    break
            else:
                could_potion_and = False
            if could_potion_and:
                rectangle.recolor("green")
            else:
                rectangle.recolor("blue")
            if active_button == 0:
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
            else:
                for elem in poti:
                    elem.rect.x = 840 + temp_x
                    elem.rect.y = 222 - round(Bar.rect.y - 222) + temp_y
                    text = font.render(str(POTIONS[elem.name]), True, "black")
                    text_x = 875 + temp_x
                    text_y = 222 + temp_y - round(Bar.rect.y - 222)
                    if temp_x == 100:
                        temp_x = 4
                        temp_y += 48
                    else:
                        temp_x += 48
                    screen.blit(text, (text_x, text_y))
            screen.blit(hero.image, camera.apply(hero))
            screen.blit(text_end, (75, 550))
            individ_board.draw(screen)
            buttons_group.draw(screen)
            moveGroup.draw(screen)
        else:
            temp = cust.rect.x
            cust.update(direc_taverna[0])
            if temp == cust.rect.x and direc_taverna[0] != -1:
                direc_taverna[0] = -1
                if temp == 700:
                    entities_taverna.add(Only_rect(200, 600, 600, 50, "red"))
            entities_taverna.draw(screen)
        mass_butt_group.draw(screen)
        # сюда надо переставить перерисовку изображения после того как я сделаю изображения прозрачными или до этого цикла поставить прорисовку кликнутого изображения
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
