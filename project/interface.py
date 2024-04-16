import pygame

PIC_FOLDER = "pictures/"


import pygame
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

screen.fill((255,255,255))



IMAGE = PIC_FOLDER + 'board.png'

img = pygame.image.load(IMAGE)
screen.blit(img, (0, 0))

pygame.display.flip()
finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

pygame.quit()