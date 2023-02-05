from load_image import load_image
from main import OnlyImage, Only_rect

import pygame as pg
fps = 60
TEXT = [["Продолжить", 200, 200], ["Новая игра", 200, 300], ["Об игре", 200, 400]]

#class my_image

if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    entities = pg.sprite.Group()
    entities.add(OnlyImage(0, 0, "backgroundstart.png"))
    running = True
    entities.draw(screen)
    pg.display.flip()
    font_text = pg.font.Font(None, 40)
    for elem in TEXT:
        text = font_text.render(elem[0], True, "black")
        screen.blit(text, (elem[1], elem[2]))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill("black")
        entities.draw(screen)
        for elem in TEXT:
            text = font_text.render(elem[0], True, "black")
            screen.blit(text, (elem[1], elem[2]))
        clock.tick(fps)
        pg.display.flip()
    pg.quit()
