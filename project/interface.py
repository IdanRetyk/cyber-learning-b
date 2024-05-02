import pygame

from classes import PIC_FOLDER,Card,Game


import pygame
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 500
pygame.init()




class GUI():
    def __init__(self) -> None:
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


        card1,card2 = Game(list()).deal_cards()

        card1: Card = card1
        card2: Card = card2

        screen.blit(card1.get_picture(),(340,435))
        screen.blit(card2.get_picture(),(355,435))
        pygame.draw.circle(screen,(255,215,0),(970,445),40)
        pygame.draw.circle(screen, (240, 176, 0),(970,445),33,5)


        pygame.font.init()
        my_font = pygame.font.SysFont('IMPACT', 30)
        screen.blit(my_font.render('BET', False, (110, 82, 35)), (950, 427))


        pygame.display.flip()
        finish = False
        while not finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    print(pos)

        pygame.quit()