import pygame as pg
from ingridient import Ingridient
from rightobject import RightThing

fps = 30


if __name__ == "__main__":
    pg.init()
    size = width, height = 800, 800
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    running = True
    entities = pg.sprite.Group()
    entities.add(Ingridient(40, 40))
    entities.add(RightThing(600, 100))
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill("black")
        entities.update()
        entities.draw(screen)
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
