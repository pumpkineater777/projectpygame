from load_image import load_image
from main import OnlyImage, Only_rect

import pygame as pg
fps = 60
TEXT = [["Продолжить", 400, 250], ["Новая игра", 400, 350], ["Об игре", 400, 450]]


if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    entities_start = pg.sprite.Group()
    entities_start.add(OnlyImage(0, 0, "backgroundstart.png"))
    running = True
    entities_start.draw(screen)
    pg.display.flip()
    font_text = pg.font.Font(None, 40)
    buttons_start = pg.sprite.Group()
    for elem in TEXT:
        text = font_text.render(elem[0], True, "black")
        screen.blit(text, (elem[1], elem[2]))
        buttons_start.add(Only_rect(elem[1] - 15, elem[2] - 15, len(elem[0]) * 20, 50, "green"))
    point_group = pg.sprite.Group()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                for elem in buttons_start:
                    if elem.mouse_over(event.pos):
                        point_group = pg.sprite.Group()
                        point_group.add(elem)
                        break
                else:
                    point_group = pg.sprite.Group()
        screen.fill("black")
        entities_start.draw(screen)
        point_group.draw(screen)
        for elem in TEXT:
            text = font_text.render(elem[0], True, "black")
            screen.blit(text, (elem[1], elem[2]))
        clock.tick(fps)
        pg.display.flip()
    pg.quit()
