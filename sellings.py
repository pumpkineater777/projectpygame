import pygame as pg

fps = 60
move_speed = 10


class Base_shape(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class customer(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((200, 200))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, direc):
        if direc == 0:
            self.rect.x -= move_speed
        elif direc == 1:
            self.rect.x += move_speed
        if self.rect.x > 1000:
            self.rect.x = 1000
        if self.rect.x < 700:
            self.rect.x = 700


if __name__ == "__main__":
    pg.init()
    size = width, height = 1000, 700
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Narkotiki")
    clock = pg.time.Clock()
    entities_taverna = pg.sprite.Group()
    entities_taverna.add(OnlyImage(0, 0, "background.png"))
    running = True
    direc_taverna = [-1, -1]
    cust = customer(800, 400)
    entities_taverna.add(cust)
    entities_taverna.draw(screen)
    font = pg.font.Font(None, 30)
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and direc_taverna[0] == -1:
                direc_taverna[0] = (direc_taverna[1] + 1) % 2
                direc_taverna[1] = direc_taverna[0]
        screen.fill("black")
        temp = cust.rect.x
        cust.update(direc_taverna[0])
        if temp == cust.rect.x and direc_taverna[0] != -1:
            direc_taverna[0] = -1
            if temp == 700:
                entities_taverna.add(Base_shape(200, 600, 600, 50, "red"))
        entities_taverna.draw(screen)
        clock.tick(fps)
        pg.display.flip()
    pg.quit()
