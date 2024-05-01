import pygame

PIC_FOLDER = "/Users/Idan/cyber-learning-b/project/pictures/"


import pygame
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 500
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

screen.fill((255,255,255))





b_bg = pygame.image.load(PIC_FOLDER + 'table_bg.JPG')
card_back = pygame.image.load(PIC_FOLDER + 'card_back.png')

screen.blit(b_bg, (0, 0))
screen.blit(card_back,(300,160))
screen.blit(card_back,(280,160))
screen.blit(card_back,(280,250))
screen.blit(card_back,(260,250))
screen.blit(card_back,(700,160))
screen.blit(card_back,(720,160))
screen.blit(card_back,(740,250))
screen.blit(card_back,(720,250))
pygame.display.flip()

finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

pygame.quit()