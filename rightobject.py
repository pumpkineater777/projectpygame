import pygame
import random

from sprites import Mouse


class Button(pygame.sprite.Sprite):
    def __init__(self, id, position):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.image = pygame.image.load('image/flower1.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def mouse_over(self, mouse):
        if self.rect.collidepoint(mouse):
            print(self.id)


pygame.init()

pygame.display.set_caption("тест")
icon_game = pygame.image.load("image/rightobject.png")
pygame.display.set_icon(icon_game)
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
mouse = Mouse((0, 0))

x = random.randint(0, 9)

heroes = pygame.sprite.Group()
heroes.add(Button(0, (0, 0)), Button(1, (100, 0)), )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            for hero in heroes:
                hero.mouse_over(event.pos)

    # if pygame.sprite.spritecollide(mouse, heroes, False):
    #     print(heroes)

    screen.fill((0, 0, 0))

    # получение координат мыши
    mouse_pos = pygame.mouse.get_pos()
    mouse.rect.x = mouse_pos[0]
    mouse.rect.y = mouse_pos[1]

    heroes.draw(screen)

    # прорисовка моего курсора и скрытие стандартного
    screen.blit(mouse.image, mouse_pos)
    pygame.mouse.set_visible(0)

    pygame.display.flip()
    clock.tick(60)

#      print(clock)


pygame.quit()