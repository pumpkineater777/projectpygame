from load_image import load_image
import pygame as pg
fps = 60

if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    entities = pg.sprite.Group()
    running = True
    entities.draw(screen)
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill("black")
        entities.draw(screen)
        clock.tick(fps)
        pg.display.flip()
    pg.quit()
