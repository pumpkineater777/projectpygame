import pygame as pg
import random
from ingridient import Ingridient
from load_image import load_image
from object import Object
from porion import Potion
from bpwl import Bowl
from ruchka import Ruchka
from sellings import customer
import sqlite3
from customer import do_path

fps = 60

left_win = 50
top_win = 50
win_width = 600
win_height = 400
poor_dict = {0: ("ingidient_", 1040), 1: ("potion_", 1127)}
poor_mass_dict = {0: ("taverna_", 0), 1: ("laborat_", 50)}
TEXT = [["Продолжить", 400, 250], ["Новая игра", 400, 350], ["Об игре", 400, 450]]
WAY_TO_HELL = "image/"
ingridient_spisok = ["letUS.png", "flower1.png"]
potion_spisok = ["potion_phot.png"]
number = 3
max_row = 410
top_left = 580
message_group = pg.sprite.Group()
message_rect = None
quit_message_rect = None
button_ok = None
button_no = None
number_selling_items = 4
can_you_click = True


class Actually_only_rect(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(color)
        self.color = color


class Only_rect(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(color)
        self.color = color

    def recolor(self, color):
        self.image.fill(color)
        self.color = color

    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            return True

    def redo(self, x, y, width, height):
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(self.color)


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


def create_message_box():
    global message_rect, quit_message_rect, button_no, button_ok, can_you_click
    message_rect = Only_rect(200, 200, 600, 400, "brown")
    quit_message_rect = Only_rect(750, 200, 50, 50, "red")
    button_ok = Only_rect(300, 500, 100, 50, "green")
    button_no = Only_rect(600, 500, 100, 50, "red")
    message_group.add(message_rect)
    message_group.add(quit_message_rect)
    message_group.add(button_ok)
    message_group.add(button_no)
    can_you_click = False


if __name__ == "__main__":
    con = sqlite3.connect(WAY_TO_HELL + "pygame.sqlite")
    cur = con.cursor()
    pg.init()
    size = width, height = 1200, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    running = True
    entities_taverna = pg.sprite.Group()
    entities_taverna.add(OnlyImage(0, 0, "background.png"))
    direc_taverna = [-1, -1]
    cust = customer(800, 400)
    id = 1
    entities_taverna.add(cust)
    entities_taverna.draw(screen)
    addiction = pg.sprite.Group()
    board = pg.sprite.Group()
    entities = pg.sprite.Group()
    map = Map(0, 0, "potioncraftmap.jpg")
    kill_map = Map(415, 250, "mapkill.png")
    addiction.add(kill_map)
    addiction.add(map)
    reading_cust_speech = 0
    board.add(Boarder(0, 0, width, top_win))
    board.add(Boarder(0, left_win, left_win, height - left_win))
    board.add(Boarder(left_win + win_width, top_win, width - (left_win + win_width), height - top_win))
    board.add(Boarder(left_win, top_win + win_height, width - left_win, height - (top_win + win_height)))
    individ_board = pg.sprite.Group()
    individ_board.add(Boarder(1000, 0, 200, 200))
    entities.add(OnlyImage(400, 417, "chunk.png"))
    tuda_ix = OnlyImage(1040, 200, "rightobject.png")
    money = [*cur.execute("""SELECT money FROM player_data where id_player = ?""", (id,))]
    money = money[0][0]
    print(money)
    entities.add(tuda_ix)
    tuda_ix_group = pg.sprite.Group()
    tuda_ix_group.add(tuda_ix)
    ruchka = Ruchka(430, 355)
    entities.add(ruchka)
    temp = Bowl(430, 420)
    entities.add(temp)
    kills = [temp]
    Bar = bar(1188, 222)
    entities.add(Bar)
    individ_board.add(Bar)
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
    temp = [*cur.execute("""SELECT * FROM customer  WHERE number = ?""", (random.randint(1, number),))]
    print(temp)
    customer_type = temp[0][1]
    customer_speech, customer_want, customer_dont_pick, customer_picked, customer_exit = temp[0][2:7]
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
    end_dialod_button = Only_rect(50, 220, 280, 70, "red")
    text_end_dialog = font_end.render("Закончить диалог", True, "black")
    screen.blit(text_end_dialog, (120, 120))
    ingr_photo = pg.sprite.Group()
    result = cur.execute(f"""SELECT * FROM ingridient_player_data
            WHERE id_player = {id}""").fetchall()
    INGR = {}
    for elem in result:
        INGR[elem[1]] = elem[2]
    gaming = False
    for elem in INGR:
        temp = Inridient_photo(1040 + temp_x, 222 + temp_y, elem)
        ingr_photo.add(temp)
        text = font.render(str(INGR[elem]), True, "black")
        text_x = 1075 + temp_x
        text_y = 222 + temp_y - (Bar.rect.y - 222)
        ingr.append(temp)
        if temp_x == 100:
            temp_x = 0
            temp_y += 48
        else:
            temp_x += 48
        screen.blit(text, (text_x, text_y))
    ingr_x = temp_x
    ingr_y = temp_y
    poti = []
    poti_photo = pg.sprite.Group()
    temp_x = 4
    temp_y = 4
    result = cur.execute(f"""SELECT * FROM potion_player_data
                WHERE id_player = {id}""").fetchall()
    POTIONS = {}
    text_message_box = ''
    font_message_box = pg.font.Font(None, 30)
    for elem in result:
        POTIONS[elem[1]] = elem[2]
    for elem in POTIONS:
        temp = Inridient_photo(1040 + temp_x, 222 + temp_y, elem)
        poti_photo.add(temp)
        text = font.render(str(POTIONS[elem]), True, "black")
        text_x = 1075 + temp_x
        text_y = 222 + temp_y - (Bar.rect.y - 222)
        poti.append(temp)
        if temp_x == 100:
            temp_x = 0
            temp_y += 48
        else:
            temp_x += 48
        screen.blit(text, (text_x, text_y))
    poti_x = temp_x
    No_WaY_nEw_ReD_bUtToN = Only_rect(50, 300, 280, 70, "red")
    no_way_new_text = font_end.render("Я тупой даун.", True, "black")
    screen.blit(no_way_new_text, (155, 220))
    poti_y = temp_y
    table_or_not = Actually_only_rect(350, 500, 300, 150, "pink")
    for e in addiction:
        screen.blit(e.image, camera.apply(e))
    entities_start = pg.sprite.Group()
    entities_start.add(OnlyImage(0, 0, "backgroundstart.png"))
    entities_start.draw(screen)
    dialog_button = pg.sprite.Group()
    dialog_button.add(end_dialod_button)
    dialog_button.add(No_WaY_nEw_ReD_bUtToN)
    pg.display.flip()
    font_text = pg.font.Font(None, 40)
    buttons_start = pg.sprite.Group()
    move_taverna_group = pg.sprite.Group()
    cust_taverna_group = pg.sprite.Group()
    buttons_start_vector = []
    font_customer = pg.font.Font(None, 20)
    for elem in TEXT:
        text = font_text.render(elem[0], True, "black")
        screen.blit(text, (elem[1], elem[2]))
        temp = Only_rect(elem[1] - 15, elem[2] - 15, len(elem[0]) * 20, 50, "green")
        buttons_start.add(temp)
        buttons_start_vector.append(temp)
    point_group = pg.sprite.Group()
    entities.draw(screen)
    individ_board.draw(screen)
    pg.display.flip()
    my_mouse = [0, 0]
    timer = 0
    no_way_new_timer = None
    arrows = pg.sprite.Group()
    tempopary = pg.sprite.Group()
    path = []
    index = 0
    read_rect = None
    font_money = pg.font.Font(None, 40)
    ingr_demand = None
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                if gaming:
                    for elem in *ingr_photo, *poti_photo:
                        if elem.mouse_over(event.pos) and event.pos[1] >= 200:
                            if (elem in ingr and active_button == 0) or (elem in poti and active_button == 1):
                                pointed = pointed[1], elem
                                break
                    else:
                        pointed = pointed[1], None
                else:
                    for elem in buttons_start:
                        if elem.mouse_over(event.pos):
                            point_group = pg.sprite.Group()
                            point_group.add(elem)
                            break
                    else:
                        point_group = pg.sprite.Group()
            if event.type == pg.MOUSEBUTTONDOWN:
                if gaming and can_you_click:
                    for elem in *entities, *moveGroup, *buttons_group, *ingr_photo, *poti_photo, *mass_butt_group, *move_taverna_group, *dialog_button, *cust_taverna_group:
                        if elem.mouse_over(event.pos):
                            mustage = True
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
                            elif elem in buttons:
                                if buttons.index(elem) != active_button:
                                    buttons[active_button].kill()
                                    buttons[active_button] = Inridient_photo(poor_dict[active_button][1], 100,
                                                                             poor_dict[active_button][
                                                                                 0] + "passive.png")
                                    buttons_group.add(buttons[active_button])
                                    active_button = buttons.index(elem)
                                    buttons[active_button].kill()
                                    buttons[active_button] = Inridient_photo(poor_dict[active_button][1], 100,
                                                                             poor_dict[active_button][
                                                                                 0] + "active.png")
                                    buttons_group.add(buttons[active_button])
                            elif elem in ingr:
                                if event.pos[1] >= 200 and active_button == 0:
                                    temp = Ingridient(elem.rect.y, elem.rect.x, elem.name, "ingr")
                                    if act_mass_butt == 1:
                                        moveGroup.add(temp)
                                    else:
                                        move_taverna_group.add(temp)
                                    clicked = temp
                                    my_mouse[1] = event.pos[1] - elem.rect.y
                                    my_mouse[0] = event.pos[0] - elem.rect.x
                                    INGR[elem.name] -= 1
                                    if INGR[elem.name] == 0:
                                        INGR.pop(elem.name)
                                        cur.execute(
                                            f"""DELETE from ingridient_player_data WHERE title = ?""", (elem.name,))
                                        elem.kill()
                                        ind = ingr.index(elem)
                                        ingr.pop(ind)
                                    else:
                                        cur.execute(
                                            f"""UPDATE ingridient_player_data SET count = {INGR[elem.name]} WHERE title = ?""",
                                            (elem.name,))
                                    con.commit()
                            elif elem in poti:
                                if event.pos[1] >= 200 and active_button == 1:
                                    temp = Ingridient(elem.rect.y, elem.rect.x, elem.name, "poti")
                                    if act_mass_butt == 1:
                                        moveGroup.add(temp)
                                    else:
                                        move_taverna_group.add(temp)
                                    clicked = temp
                                    my_mouse[1] = event.pos[1] - elem.rect.y
                                    my_mouse[0] = event.pos[0] - elem.rect.x
                                    POTIONS[elem.name] -= 1
                                    if POTIONS[elem.name] == 0:
                                        POTIONS.pop(elem.name)
                                        elem.kill()
                                        cur.execute(
                                            f"""DELETE from potion_player_data WHERE title = ?""", (elem.name,))
                                        ind = poti.index(elem)
                                        poti.pop(ind)
                                    else:
                                        cur.execute(
                                            f"""UPDATE potion_player_data SET count = {POTIONS[elem.name]} WHERE title = ?""",
                                            (elem.name,))
                                    con.commit()
                                can_you_click = True
                            elif elem == Bar or elem in move_taverna_group or elem in cust_taverna_group:
                                clicked = elem
                                my_mouse[1] = event.pos[1] - elem.rect.y
                                my_mouse[0] = event.pos[0] - elem.rect.x
                            else:
                                mustage = False
                            if act_mass_butt == 1 and not mustage:
                                if elem == rectangle:
                                    if could_potion_and:
                                        hero.set_coords(1284, 1284)
                                        if could_potion_and.potion in POTIONS:
                                            POTIONS[could_potion_and.potion] += 1
                                            cur.execute(
                                                f"UPDATE potion_player_data SET count = {POTIONS[could_potion_and.potion]} WHERE title = ?",
                                                (could_potion_and.potion,))
                                        else:
                                            POTIONS[could_potion_and.potion] = 1
                                            cur.execute(
                                                f"""INSERT INTO potion_player_data VALUES(?, ?, 1)""",
                                                (id, could_potion_and.potion))
                                            temp = Inridient_photo(1040 + poti_x, 222 + poti_y, could_potion_and.potion)
                                            poti_photo.add(temp)
                                            poti.append(temp)
                                            if poti_x == 100:
                                                poti_x = 0
                                                poti_y += 48
                                            else:
                                                poti_x += 48
                                        con.commit()
                                        for i in big_path:
                                            i.kill()
                                        big_path = []
                                        path = []
                                        could_potion_and = False
                                        index = 0
                                elif elem == discard_button:
                                    can_you_click = False
                                    create_message_box()
                                    hero.set_coords(1284, 1284)
                                    for i in big_path:
                                        i.kill()
                                    big_path = []
                                    path = []
                                    index = 0
                                    text_message_box = "Вы хотите сбросить зелье? Все ингридиенты будут утрачены"
                                elif elem == ruchka or elem in moveGroup:
                                    clicked = elem
                                    my_mouse[1] = event.pos[1] - elem.rect.y
                                    my_mouse[0] = event.pos[0] - elem.rect.x
                            elif not mustage and (reading_cust_speech == 1 or reading_cust_speech == 4):
                                if elem == end_dialod_button:
                                    if reading_cust_speech == 1 or reading_cust_speech == 4:
                                        reading_cust_speech = 2
                                        read_rect.redo(top_left, 400 - (len(customer_exit) + 52) // 53 * 20, max_row,
                                                       (len(customer_exit) + 52) // 53 * 20)
                                        for i in cust_taverna_group:
                                            i.kill()
                                elif elem == No_WaY_nEw_ReD_bUtToN:
                                    no_way_new_timer = 0
                                    arrows.add(OnlyImage(800, 300, "arrow_right.png"))
                                    arrows.add(OnlyImage(400, 300, "arrow_down.png"))
                elif not can_you_click:
                    if quit_message_rect.mouse_over(event.pos):
                        for elem in message_group:
                            elem.kill()
                        message_rect = None
                        quit_message_rect = None
                        can_you_click = True
                        if ingr_demand:
                            ingr_demand.set_coords()

                    #if quit-messafe
                else:
                    for elem in point_group:
                        if buttons_start_vector.index(elem) == 0:
                            gaming = True
            if event.type == pg.KEYDOWN:
                if gaming:
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
                            if reading_cust_speech == 2 or reading_cust_speech == 3:
                                read_rect.kill()
                                read_rect = None
                                temp = [*cur.execute("""SELECT * FROM customer  WHERE number = ?""",
                                                     (random.randint(1, number),))]
                                customer_type = temp[0][1]
                                customer_speech, customer_want, customer_dont_pick, customer_picked, customer_exit = \
                                    temp[0][2:7]
                            if reading_cust_speech != 1 and reading_cust_speech != 4:
                                if direc_taverna[0] == -1:
                                    direc_taverna[0] = (direc_taverna[1] + 1) % 2
                                    direc_taverna[1] = direc_taverna[0]
                                reading_cust_speech = 0
                    if event.key == pg.K_ESCAPE:
                        gaming = False
            if event.type == pg.KEYUP:
                if gaming:
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
                if gaming:
                    if clicked != Bar and clicked:
                        if (pg.sprite.collide_rect(clicked, tuda_ix) and act_mass_butt == 1) or (
                                not pg.sprite.collide_rect(clicked,
                                                           table_or_not) and act_mass_butt == 0 and reading_cust_speech == 1) or (
                                act_mass_butt == 0 and not (reading_cust_speech == 1 or reading_cust_speech == 4)):
                            if clicked in cust_taverna_group:
                                create_message_box()
                                ingr_money = [
                                    *cur.execute("SELECT cost FROM ingridient where title = ?", (clicked.name,))]
                                ingr_money = ingr_money[0][0]
                                text_message_box = f"Вы хотите купить этот ингридиент за {ingr_money}?"
                                ingr_demand = clicked
                            elif clicked.name in INGR:
                                INGR[clicked.name] += 1
                                cur.execute(
                                    f"UPDATE ingridient_player_data SET count = {INGR[clicked.name]} WHERE title = ?",
                                    (clicked.name,))
                            elif clicked.name in ingridient_spisok:
                                INGR[clicked.name] = 1
                                cur.execute(
                                    f"""INSERT INTO ingridient_player_data VALUES(?, ?, 1)""",
                                    (id, clicked.name))
                                temp = Inridient_photo(1040 + ingr_x, 222 + ingr_y, clicked.name)
                                ingr_photo.add(temp)
                                ingr.append(temp)
                                if ingr_x == 100:
                                    ingr_x = 0
                                    ingr_y += 48
                                else:
                                    ingr_x += 48
                            elif clicked.name in POTIONS:
                                POTIONS[clicked.name] += 1
                                cur.execute(
                                    f"UPDATE potion_player_data SET count = {POTIONS[clicked.name]} WHERE title = ?",
                                    (clicked.name,))
                            elif clicked.name in potion_spisok:
                                POTIONS[clicked.name] = 1
                                cur.execute(
                                    f"""INSERT INTO potion_player_data VALUES(?, ?, 1)""",
                                    (id, clicked.name))
                                temp = Inridient_photo(1040 + poti_x, 222 + poti_y, clicked.name)
                                poti_photo.add(temp)
                                poti.append(temp)
                                if poti_x == 100:
                                    poti_x = 0
                                    poti_y += 48
                                else:
                                    poti_x += 48
                            if not clicked in cust_taverna_group:
                                clicked.kill()
                            con.commit()
                        elif act_mass_butt == 0 and customer_type == 0:
                            if customer_want == clicked.name:
                                clicked.kill()
                                reading_cust_speech = 3
                                read_rect.redo(top_left, 400 - (len(customer_picked) + 52) // 53 * 20, max_row,
                                               (len(customer_picked) + 52) // 53 * 20)
                            elif customer_want != clicked.name:
                                if reading_cust_speech != 4:
                                    reading_cust_speech = 4
                                    read_rect.redo(top_left, 400 - (len(customer_dont_pick) + 52) // 53 * 20, max_row,
                                                   (len(customer_dont_pick) + 52) // 53 * 20)
                                else:
                                    reading_cust_speech = 2
                                    read_rect.redo(top_left, 400 - (len(customer_dont_pick) + 52) // 53 * 20, max_row,
                                                   (len(customer_dont_pick) + 52) // 53 * 20)
                                clicked.kill()
                                if clicked.name in INGR:
                                    INGR[clicked.name] += 1
                                    cur.execute(
                                        f"UPDATE ingridient_player_data SET count = {INGR[clicked.name]} WHERE title = ?",
                                        (clicked.name,))
                                elif clicked.name in ingridient_spisok:
                                    INGR[clicked.name] = 1
                                    cur.execute(
                                        f"""INSERT INTO ingridient_player_data VALUES(?, ?, 1)""",
                                        (id, clicked.name))
                                    temp = Inridient_photo(1040 + ingr_x, 222 + ingr_y, clicked.name)
                                    ingr_photo.add(temp)
                                    ingr.append(temp)
                                    if ingr_x == 100:
                                        ingr_x = 0
                                        ingr_y += 48
                                    else:
                                        ingr_x += 48
                                elif clicked.name in POTIONS:
                                    POTIONS[clicked.name] += 1
                                    cur.execute(
                                        f"UPDATE potion_player_data SET count = {POTIONS[clicked.name]} WHERE title = ?",
                                        (clicked.name,))
                                elif clicked.name in potion_spisok:
                                    POTIONS[clicked.name] = 1
                                    cur.execute(
                                        f"""INSERT INTO potion_player_data VALUES(?, ?, 1)""",
                                        (id, clicked.name))
                                    temp = Inridient_photo(1040 + poti_x, 222 + poti_y, clicked.name)
                                    poti_photo.add(temp)
                                    poti.append(temp)
                                    if poti_x == 100:
                                        poti_x = 0
                                        poti_y += 48
                                    else:
                                        poti_x += 48
                                con.commit()
                clicked = None
        screen.fill("black")
        if gaming:
            if act_mass_butt == 1:
                if pointed[0] == pointed[1] != None:
                    timer += 1
                else:
                    timer = 0
                    for elem in tempopary:
                        elem.kill()
                if timer == 50:
                    if (pointed[0] in ingr or pointed[0] in poti):
                        temp = OnlyImage(pointed[0].rect.x - 75, pointed[0].rect.y + 50,
                                         [*cur.execute("""SELECT pointed_photo FROM ingridient WHERE title = ?""",
                                                       (pointed[0].name,))][0][0])
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
                                temp = cur.execute("""SELECT * FROM ingridient WHERE title = ?""", (self.name,))
                                name, pointed_photo, path_photo, spisok = [*temp][0]
                                spisok = [float(elem) for elem in spisok.split('#')]
                                path.append(do_path(spisok))
                                temp = OnlyImage(hero.rect.x - 30, hero.rect.y + 10, path_photo)
                                addiction.add(temp)
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
                    print(10)
                    mouse_pos = pg.mouse.get_pos()
                    clicked.update_mouse(mouse_pos, my_mouse)
                for e in addiction:
                    screen.blit(e.image, camera.apply(e))
                board.draw(screen)
                entities.draw(screen)
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
                screen.blit(hero.image, camera.apply(hero))
                screen.blit(text_end, (75, 550))
            else:
                temp = cust.rect.x
                cust.update(direc_taverna[0])
                if temp == cust.rect.x and direc_taverna[0] != -1:
                    direc_taverna[0] = -1
                    if temp == 700:
                        read_rect = Only_rect(top_left, 400 - (len(customer_speech) + 52) // 53 * 20, max_row,
                                              (len(customer_speech) + 52) // 53 * 20, "black")
                        entities_taverna.add(read_rect)
                        reading_cust_speech = 1
                        if customer_type == 1:
                            for i in range(number_selling_items):
                                cust_taverna_group.add(Ingridient(
                                    random.randint(table_or_not.rect.x, table_or_not.rect.x + table_or_not.rect.width),
                                    random.randint(table_or_not.rect.y, table_or_not.rect.y + table_or_not.rect.height),
                                    random.choice(ingridient_spisok), ingr))
                        """
                        answer_rect = Only_rect(50, 300, 250, 100, "black")
                        entities_taverna.add(answer_rect)
                        """
                entities_taverna.draw(screen)
            if act_mass_butt == 0:
                tuda_ix_group.draw(screen)
            temp_x = 4
            temp_y = 4
            if active_button == 0:
                ingr_photo.draw(screen)
                for elem in ingr:
                    elem.rect.x = 1040 + temp_x
                    elem.rect.y = 222 - round(Bar.rect.y - 222) + temp_y
                    text = font.render(str(INGR[elem.name]), True, "black")
                    text_x = 1075 + temp_x
                    text_y = 222 + temp_y - round(Bar.rect.y - 222)
                    if temp_x == 100:
                        temp_x = 4
                        temp_y += 48
                    else:
                        temp_x += 48
                    screen.blit(text, (text_x, text_y))
            else:
                poti_photo.draw(screen)
                for elem in poti:
                    elem.rect.x = 1040 + temp_x
                    elem.rect.y = 222 - round(Bar.rect.y - 222) + temp_y
                    text = font.render(str(POTIONS[elem.name]), True, "black")
                    text_x = 1075 + temp_x
                    text_y = 222 + temp_y - round(Bar.rect.y - 222)
                    if temp_x == 100:
                        temp_x = 4
                        temp_y += 48
                    else:
                        temp_x += 48
                    screen.blit(text, (text_x, text_y))
            individ_board.draw(screen)
            mass_butt_group.draw(screen)
            buttons_group.draw(screen)
            temp = font_money.render(str(money), True, "black")
            screen.blit(temp, (1100, 20))
            if act_mass_butt == 0:
                if no_way_new_timer != None:
                    no_way_new_timer += 1
                    if no_way_new_timer == 30:
                        no_way_new_timer = None
                        for elem in arrows:
                            elem.kill()
                if reading_cust_speech == 1:
                    temp = customer_speech.split()
                    dialog_button.draw(screen)
                    screen.blit(text_end_dialog, (70, 240))
                    screen.blit(no_way_new_text, (90, 320))
                    text_appender = ""
                    tyta_y = 402 - (len(customer_speech) + 52) // 53 * 20
                    for elem in temp:
                        text_appender += elem + ' '
                        if len(text_appender) >= 53:
                            text = font_customer.render(text_appender, True, "orange")
                            screen.blit(text, (top_left + 5, tyta_y))
                            tyta_y += 20
                            text_appender = ""
                    if text_appender:
                        text = font_customer.render(text_appender, True, "orange")
                        screen.blit(text, (top_left + 5, tyta_y))
                elif reading_cust_speech == 2:
                    temp = customer_exit.split()
                    text_appender = ""
                    tyta_y = 402 - (len(customer_exit) + 52) // 53 * 20
                    for elem in temp:
                        text_appender += elem + ' '
                        if len(text_appender) >= 53:
                            text = font_customer.render(text_appender, True, "orange")
                            screen.blit(text, (top_left + 5, tyta_y))
                            tyta_y += 20
                            text_appender = ""
                    if text_appender:
                        text = font_customer.render(text_appender, True, "orange")
                        screen.blit(text, (top_left + 5, tyta_y))
                elif reading_cust_speech == 3:
                    temp = customer_picked.split()
                    text_appender = ""
                    tyta_y = 402 - (len(customer_picked) + 52) // 53 * 20
                    for elem in temp:
                        text_appender += elem + ' '
                        if len(text_appender) >= 53:
                            text = font_customer.render(text_appender, True, "orange")
                            screen.blit(text, (top_left + 5, tyta_y))
                            tyta_y += 20
                            text_appender = ""
                    if text_appender:
                        text = font_customer.render(text_appender, True, "orange")
                        screen.blit(text, (top_left + 5, tyta_y))
                elif reading_cust_speech == 4:
                    temp = customer_dont_pick.split()
                    dialog_button.draw(screen)
                    screen.blit(text_end_dialog, (70, 240))
                    screen.blit(no_way_new_text, (90, 320))
                    text_appender = ""
                    tyta_y = 402 - (len(customer_dont_pick) + 52) // 53 * 20
                    for elem in temp:
                        text_appender += elem + ' '
                        if len(text_appender) >= 53:
                            text = font_customer.render(text_appender, True, "orange")
                            screen.blit(text, (top_left + 5, tyta_y))
                            tyta_y += 20
                            text_appender = ""
                    if text_appender:
                        text = font_customer.render(text_appender, True, "orange")
                        screen.blit(text, (top_left + 5, tyta_y))
                arrows.draw(screen)
            if act_mass_butt == 1:
                moveGroup.draw(screen)
            else:
                if clicked != None:
                    print(111)
                    mouse_pos = pg.mouse.get_pos()
                    clicked.update_mouse(mouse_pos, my_mouse)
                move_taverna_group.draw(screen)
                cust_taverna_group.draw(screen)
            message_group.draw(screen)
            if not can_you_click:
                text_appender = ""
                tyta_y = 300
                temp = text_message_box.split()
                typical_left = 250
                for elem in temp:
                    text_appender += elem + ' '
                    if len(text_appender) >= 46:
                        text = font_message_box.render(text_appender, True, "orange")
                        screen.blit(text, (typical_left, tyta_y))
                        tyta_y += 30
                        text_appender = ""
                if text_appender:
                    text = font_message_box.render(text_appender, True, "orange")
                    screen.blit(text, (typical_left, tyta_y))
                temp = font_message_box.render("ДА", True, "brown")
                screen.blit(temp, (330, 515))
                temp = font_message_box.render("НЕТ", True, "brown")
                screen.blit(temp, (630, 515))
        else:
            entities_start.draw(screen)
            point_group.draw(screen)
            for elem in TEXT:
                text = font_text.render(elem[0], True, "black")
                screen.blit(text, (elem[1], elem[2]))
        # сюда надо переставить перерисовку изображения после того как я сделаю изображения прозрачными или до этого цикла поставить прорисовку кликнутого изображения
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
    con.close()
# будем считать что на строке в 200 пикселей помещаеться максимум 26 букв, чтобы было красиво
# 1 буква двадцатого фонта размером в 200 / 28.3 пикселя при чем если буква заглавная на нее больше места тратиться чем на маленькую, абсолютно отвратильно просто отвратительно
