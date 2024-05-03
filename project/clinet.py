import pygame

from classes import PIC_FOLDER,Card,Game
from functions import sub_tuple


WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 500
pygame.init()

BET_POS: tuple[int,int] = (970,445)


class GUI():
    

    
    def __init__(self) -> None:
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")

        self.screen.fill((255,255,255))





        b_bg = pygame.image.load(PIC_FOLDER + 'table_bg.JPG')
        card_back = pygame.image.load(PIC_FOLDER + 'card_back.png')

        self.screen.blit(b_bg, (0, 0))
        self.screen.blit(card_back,(300,160))
        self.screen.blit(card_back,(280,160))
        self.screen.blit(card_back,(280,250))
        self.screen.blit(card_back,(260,250))
        self.screen.blit(card_back,(700,160))
        self.screen.blit(card_back,(720,160))
        self.screen.blit(card_back,(740,250))
        self.screen.blit(card_back,(720,250))


        card1,card2 = Game(list()).deal_cards()

        card1: Card = card1
        card2: Card = card2

        self.screen.blit(card1.get_picture(),(340,435))
        self.screen.blit(card2.get_picture(),(355,435))
        pygame.draw.circle(self.screen,(255,215,0),BET_POS,40)
        pygame.draw.circle(self.screen, (240, 176, 0),BET_POS,33,5)


        pygame.font.init()
        my_font = pygame.font.SysFont('IMPACT', 30)
        self.screen.blit(my_font.render('BET', False, (110, 82, 35)), (950, 427))


        pygame.display.flip()
        finish = False
        while not finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                # If left click is pressed - check where player clicked.
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    distance_from_bet = sub_tuple(pos,BET_POS)
                    if distance_from_bet[0] < 35 and distance_from_bet[1] < 35:
                        self.show_bet_menu()
                    else:
                        print(pos)
        pygame.quit()
    
    
    def show_bet_menu(self):
        print("BET")
        #TODO implement this



if __name__ == "__main__":
    GUI()