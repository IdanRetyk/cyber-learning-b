import pygame,socket,traceback,pickle

from classes import PIC_FOLDER,Card,Game,Player
from functions import *
from db_server import PLAYER_COUNT

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 500
pygame.init()

BET_POS: tuple[int,int] = (970,445)
TO_SEND: bytes = b''




class GUI():
    def __init__(self,ip) -> None:
        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")
        

        finish = True

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        
        port = 1235
        self.ADDR = (ip,port)
        try:
            self.sock.connect((ip,port))
            print (f'Connect succeeded {ip}:{port}')
            finish = False
        except:
            print(f'Error while trying to connect.  Check ip or port -- {ip}:{port}')
        
        
        # Client Hello
        #TODO money,name in gui.
        money = 100
        name = "Idan"
        send_data(self.sock,f"HELLO~{money}~{name}".encode(),(ip,port))
        

        from_server,a = recive_by_size(self.sock)
        code,player_remaining = from_server.split(b'~')
        
        if code != b"HELLO":
            raise ValueError("Expecting hello, instead received ", code)
        while(code == b"HELLO"):
            print(f"waiting for players, {player_remaining} remaining...")
            from_server,a = recive_by_size(self.sock)
            code,player_remaining = from_server.split(b'~')
        # Handshake complete, ready to start game
        
        from_server,a = recive_by_size(self.sock)
        code,player_pickle= from_server.split(b'~')
        if code != b"PLYR":
            raise ValueError("Expecting hello, instead received ", code)
        self.player: Player = pickle.loads(player_pickle)
        
        self.load_images()
        pygame.display.flip()
        
        
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
        self.sock.close()
    
    def load_images(self):
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

        card1, card2 = self.player.get_cards()

        self.screen.blit(card1.get_picture(),(340,435))
        self.screen.blit(card2.get_picture(),(355,435))
        pygame.draw.circle(self.screen,(255,215,0),BET_POS,40)
        pygame.draw.circle(self.screen, (240, 176, 0),BET_POS,33,5)


        pygame.font.init()
        my_font = pygame.font.SysFont('IMPACT', 30)
        self.screen.blit(my_font.render('BET', False, (110, 82, 35)), (950, 427))
    
    
    def show_bet_menu(self):
        #TODO how much player bet
        amount = 0
        
        to_send = b'MOVE~BET~' + str(amount).encode()
        send_data(self.sock,to_send,self.ADDR)
        print("BET")
        #TODO implement this


def protocol_build_request(from_user) -> str:
    """
    build the request according to user selection and protocol
    return: string - msg code
    """
    
    print("protocol_build_request not implemented")
    return str()


def protocol_parse_reply(reply) -> str:
    """
    parse the server reply and prepare it to user
    return: answer from server string
    """
    print("protocol_parse_reply not implemented")
    return str()





if __name__ == "__main__":
    GUI("127.0.0.1")