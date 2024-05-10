import pygame,socket,traceback,pickle
from base64 import b64decode

from classes import PIC_FOLDER,Card,Game,Player
from functions import *
from game_server import PLAYER_COUNT

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 500
pygame.init()

BET_POS: tuple[int,int] = (970,445)
TO_SEND: bytes = b''




class GUI():
    def __init__(self,ip) -> None:

        

        finish = False

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        
        port = 1235
        self.ADDR = (ip,port)
        
        pickleld_game,player_index = self.client_hello()
        
        self.index = int(player_index) # self.index is the player index within self.game.get_players()
        
        # When getting to this point, the last message sent is "game" message, .
        self.game : Game = pickle.loads(b64decode(pickleld_game))
        self.player = self.game.get_players()[int(player_index)]
        
        d,_ = udp_recv(self.sock)
        while d != b'ACK':
            send_data(self.sock,b'ACK',self.ADDR)
            d,_ = udp_recv(self.sock)
        
        
        # Handshake complete, ready to start game

        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")
        
        
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
    
    def client_hello(self) ->tuple[bytes,bytes]:
        # Client Hello
        #TODO money,name in gui.
        money = 100
        name = "Idan"
        from_server = None
        while from_server is None:
            send_data(self.sock,f"HELLO~{money}~{name}".encode(),self.ADDR)
            from_server,a = udp_recv(self.sock)
        
        code,player_remaining = from_server.split(b'~') # type:ignore
        
        if code != b"HELLO":
            raise ValueError("Expecting hello, instead received ", code)
        while(code == b"HELLO"):
            print(f"waiting for players, {player_remaining} remaining...")
            from_server,a = udp_recv(self.sock)
            if from_server is not None:
                fields = from_server.split(b'~')# type:ignore
                code = fields[0]
                #according to code unpack the rest of the msg
                if code == b"HELLO":
                    player_remaining = fields[1]
                elif code == B"GAME":
                    _,pickled_game,player_index = fields
                else:
                    raise ValueError("Don't know this code. msg -", from_server)
        
        return pickled_game,player_index # type:ignore
    
    
    def load_images(self):
        self.screen.fill((255,255,255))
        
        # back ground and other player's cards (hidden)
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

        # Show my cards
        card1, card2 = self.player.get_hand()

        self.screen.blit(card1.get_picture(),(340,435))
        self.screen.blit(card2.get_picture(),(355,435))
        
        pygame.font.init()
        
        # Other players' names, and money
        # TODO this works only for two players rn
        ariel = pygame.font.SysFont("Ariel",22)
        for i in range(self.index):
            self.screen.blit(ariel.render(self.game.get_players()[i].get_name(),False,(255,255,255)),(193,392))
            self.screen.blit(ariel.render(str(self.game.get_players()[i].get_money()) + '$',False,(255,255,255)),(273,302))
        for i in range(self.index + 1, len(self.game.get_players())):
            self.screen.blit(ariel.render(self.game.get_players()[i].get_name(),False,(255,255,255)),(193,392))
            self.screen.blit(ariel.render(str(self.game.get_players()[i].get_money()) + '$',False,(255,255,255)),(273,302))
        
        
        # Bet button        
        pygame.draw.circle(self.screen,(255,215,0),BET_POS,40)
        pygame.draw.circle(self.screen, (240, 176, 0),BET_POS,33,5)

        impact = pygame.font.SysFont('IMPACT', 30)
        self.screen.blit(impact.render('BET', False, (110, 82, 35)), (950, 427))
    
    
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