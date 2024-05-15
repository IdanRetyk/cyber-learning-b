import time
import pygame,socket,traceback,pickle,random
from base64 import b64decode
from PIL import Image

from classes import PIC_FOLDER,Card,Game,Player
from functions import *
from game_server import PLAYER_COUNT

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 500
pygame.init()

BET_POS: tuple[int,int] = (970,445)
CHECK_POS: tuple[int,int] = (970,345)
X_POS :tuple[int,int] = (870,445)
PLUS_POS: tuple[int,int] = (30,450)
MINUS_POS: tuple[int,int] = (100,450)



class GUI():
    def __init__(self,ip) -> None:
        finish = False
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        self.ADDR = (ip,1235)
        
        pickleld_game,player_index = self.client_hello()
        
        self.index = int(player_index) # self.index is the player index within self.game.get_players()
        
        # When getting to this point, the last message sent is "game" message, .
        self.game : Game = pickle.loads(b64decode(pickleld_game))
        self.player = self.game.get_players()[int(player_index)]
        
        d,_ = recv_ack(self.sock,"GAME") # Until changing client hello this line is necessary for some reason
        # Handshake complete, ready to start game

        size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")
        
        self.load_images()        
        self.pos = self.player.get_position()
        
        blinds(self.game)
        
        while not finish:
            self.update_gui()
            
            from_server,_ = recv_ack(self.sock,["MOVE","TURN","CARDS","EXIT","WINNER"])
            fields = from_server.split(b'~') #type:ignore
            code = fields[0]
            if code == b'EXIT':
                finish = True
                continue
            if code == b'WINNER':
                winner_list = [int(f) for f in fields[1:]]
                
                self.win(winner_list)
            
                finish = True
                
                # Add all bets to pot
                for player in self.game.get_players():
                    self.game.change_pot(player.get_curr_bet())
                    player.set_curr_bet(0)
                self.update_gui(winner_list)
                time.sleep(5)
                
                continue
            if code == b'CARDS':
                # Show cards
                self.show_community_cards(pickle.loads(b64decode(fields[1])))
                # Prepare the next round of betting
                self.game.set_bet_size(0)
                for player in self.game.get_players():
                    self.game.change_pot(player.get_curr_bet())
                    player.set_curr_bet(0)
                # Delete in gui players bet
                for i in range(self.index,self.index + 5):
                    i %= 5
                    try:
                        self.game.get_players()[i] 
                        ariel = pygame.font.SysFont("Ariel",22)
                        self.screen.blit(ariel.render("       ",False,(255,255,0),(220,0,0)),self.bet_loc[i])
                    except:
                        pass
            if code == b'MOVE':
                self.do_move(from_server) #type:ignore
            if code == b'TURN': # Input player move
                to_send: bytes = b"Undefined"
                show_bet_menu: bool = False
                while to_send == b"Undefined":
                    if fields[1] == b'0':
                        self.show_button("xcheckbet")
                    else:
                        self.show_button("xraisecall")
                        
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            finish = True
                        
                        # If left click is pressed - check where player clicked.
                        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                            pos = pygame.mouse.get_pos()
                            
                            # Check if pressed X
                            distance_from_x = sub_tuple(pos,X_POS)
                            if distance_from_x[0] < 35 and distance_from_x[1] < 35:
                                # X
                                to_send = b"MOVE~-1"
                                break
                            
                            
                            # Check if pressed check/call
                            distance_from_check = sub_tuple(pos,CHECK_POS)
                            if distance_from_check[0] < 35 and distance_from_check[1] < 35:
                                # CHECK,CALL 
                                to_send = b'MOVE~' + str(self.game.get_bet_size()).encode()
                                break                   
                            
                            # Check if pressed bet/raise
                            distance_from_bet = sub_tuple(pos,BET_POS)
                            if distance_from_bet[0] < 35 and distance_from_bet[1] < 35:
                                # Bet
                                
                                # Need to chose how much to bet.
                                if not show_bet_menu:
                                    show_bet_menu = True
                                    self.min_bet = self.game.get_bet_size()
                                    self.max_bet = self.player.get_money()
                                    self.amount = max(self.min_bet * 2,self.game.get_blind(True))
                                    self.show_bet_menu()
                                else:
                                    show_bet_menu = False
                                    to_send = f'MOVE~{self.amount}~{self.index}'.encode()
                            
                            if show_bet_menu:
                                distance_from_minus = sub_tuple(pos,MINUS_POS)
                                distance_from_plus = sub_tuple(pos,PLUS_POS)
                                if distance_from_minus[0] < 25 and distance_from_minus[1] < 25:
                                    # Minus pressed
                                    self.amount -= max(self.min_bet,self.game.get_blind(True))
                                elif distance_from_plus[0] < 25 and distance_from_plus[1] < 25:
                                    # Plus pressed
                                    self.amount += max(self.min_bet,self.game.get_blind(True))
                                self.amount = min(max(self.amount,self.min_bet),self.max_bet) # Makes sure that min_bet <= amount <= max_bet
                                ariel = pygame.font.SysFont("Ariel",30)
                                self.screen.blit(ariel.render(str(self.amount) + '$',False,(255,255,255),(0,0,0)),(55,450))
                                
                                pygame.display.flip()
                                
                                
                self.delete_buttons()
                send_data_ack(self.sock,to_send,self.ADDR,None) #type:ignore

        pygame.quit()
        self.sock.close()
    
    def client_hello(self) ->tuple[bytes,bytes]:
        # Client Hello
        #TODO money,name in gui.
        money = random.randint(80,120)
        name = random.choice(["Idan","Yossi","Ophir","Emil","Alice","Bob"])
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
    
    def win(self,winner_list: list[int]):
        pot = self.game.empty_pot()
        for player in self.game.get_players():
                pot += player.get_curr_bet()
        
        for winner_index in winner_list:
            self.game.get_players()[winner_index].change_money(pot // len(winner_list)) # Transfer money in the pot into winner's money
    
    def update_gui(self,winner_index_list:list[int] = []):
        # Show pot
        ariel = pygame.font.SysFont("Ariel",22)
        self.screen.blit(ariel.render(str(self.game.get_pot()) + '$',False,(255,255,255),(220,0,0)),(465,177))
        
        
        # Other players' name and money
        name_loc = [(442,470),(193,392),(220,24),(675,24),(759,392)]
        name_loc = name_loc[5 - self.index:] + name_loc[:5 - self.index] # Rotate list 
        money_loc = [(445,298),(276,302),(269, 141),(685, 140),(705, 303)]
        money_loc = money_loc[5 - self.index:] + money_loc[:5 - self.index]
        bet_loc = [(509, 279),(334, 254),(379, 191),(642, 202),(637, 268)]
        self.bet_loc = bet_loc[5 - self.index:] + bet_loc[:5 - self.index]
        
        for i in range(self.index,self.index + 5):
            i %= 5
            try:
                if self.game.get_players()[i].is_playing():
                    bet_color = (255,255,0)
                    if i in winner_index_list:
                        color = (0,255,0)
                    else:
                        
                        color = (255,255,255) # White
                else:
                    color = (100,100,100) # Grey
                    bet_color = (128,0,0)
                
                self.screen.blit(ariel.render(self.game.get_players()[i].get_name(),False,color,(0,0,0)),name_loc[i])
                self.screen.blit(ariel.render(str(self.game.get_players()[i].get_money()) + '$',False,color,(220,0,0)),money_loc[i])
                if self.game.get_players()[i].get_curr_bet(): # Player bet
                    self.screen.blit(ariel.render(str(self.game.get_players()[i].get_curr_bet()) + '$',False,bet_color,(220,0,0)),self.bet_loc[i])
            except Exception as e:
                pass
        pygame.display.flip()
    
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
    
    def delete_buttons(self):
        im = Image.open(PIC_FOLDER + "table_bg.JPG")
        im = im.crop((800,310,1024,500))
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        pic = pygame.image.fromstring(im.tobytes(),im.size,"RGBA")
        self.screen.blit(pic,(800,310))
        
        im = Image.open(PIC_FOLDER + "table_bg.JPG")
        im = im.crop((0,400,200,500))
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        pic = pygame.image.fromstring(im.tobytes(),im.size,"RGBA")
        self.screen.blit(pic,(0,400))
        
        pygame.display.flip()
    
    def do_move(self,move : bytes):
        """
        first calculate and update game object
        than show in gui the move.
        """
        code,move_number,p_index = move.split(b'~')
        curr_player = self.game.get_players()[int(p_index)]
        
        if move_number == b'0':
            type_ = "check"
            ariel = pygame.font.SysFont("Ariel",22)
            self.screen.blit(ariel.render("  V  ",False,(0,0,255),(220,0,0)),self.bet_loc[int(p_index)])
        elif move_number == b'-1':
            type_ = "fold"
            x_font = pygame.font.SysFont('Verdana', 15)
            self.screen.blit(x_font.render(" X ",False,(128,0,0),(220,0,0)),self.bet_loc[int(p_index)])
            curr_player.fold()
        else:
            type_ = "bet" # Or call
            amount = int(move_number) - curr_player.get_curr_bet()
            curr_player.change_money(-amount)
            curr_player.set_curr_bet(int(move_number))
            self.game.set_bet_size(int(move_number))
        
        pygame.display.flip()
    
    def show_button(self,button_str: str):
        if "check" in button_str:
            pygame.draw.circle(self.screen,(50,50,255),CHECK_POS,40)
            impact = pygame.font.SysFont('IMPACT', 28)
            self.screen.blit(impact.render('CHECK', False, (100, 110, 255)), (931,327))
            
        elif "call" in button_str:
            pygame.draw.circle(self.screen,(50,50,255),CHECK_POS,40)
            impact = pygame.font.SysFont('IMPACT', 28)
            self.screen.blit(impact.render('CALL', False, (100, 110, 255)), (940,327))
            impact = pygame.font.SysFont('IMPACT', 18)
            self.screen.blit(impact.render(str(self.game.get_bet_size() - self.player.get_curr_bet()) + '$', False, (100, 110, 255)), (948,350))
        
        if "x" in button_str:
            pygame.draw.circle(self.screen,(255,0,0),X_POS,40)
            impact = pygame.font.SysFont('Verdana', 50)
            self.screen.blit(impact.render('X', False, (128, 0, 0)), (852,415))
        
        if "bet" in button_str:
            pygame.draw.circle(self.screen,(255,215,0),BET_POS,40)
            pygame.draw.circle(self.screen, (240, 176, 0),BET_POS,33,5)

            impact = pygame.font.SysFont('IMPACT', 30)
            self.screen.blit(impact.render('BET', False, (110, 82, 35)), (950, 427))
        
        if "raise" in button_str:
            pygame.draw.circle(self.screen,(255,215,0),BET_POS,40)
            pygame.draw.circle(self.screen, (240, 176, 0),BET_POS,33,5)

            impact = pygame.font.SysFont('IMPACT', 26)
            self.screen.blit(impact.render('RAISE', False, (110, 82, 35)), (950, 427))
        
        pygame.display.flip()
        
    def show_community_cards(self,cards: list[Card]):
        x,y = (373,208)
        for card in cards:
            self.screen.blit(card.get_picture(),(x,y))
            x += 40
        pygame.display.flip()
    
    
    def show_bet_menu(self):
        plus = pygame.image.load(PIC_FOLDER + "plus.jpeg")
        minus = pygame.image.load(PIC_FOLDER + "minus.jpeg")
        
        self.screen.blit(plus,PLUS_POS)
        self.screen.blit(minus,MINUS_POS)
        
        ariel = pygame.font.SysFont("Ariel",22)
        self.screen.blit(ariel.render("0$",False,(255,255,255),(0,0,0)),(55,450))
                                
        pygame.display.flip()
    




def protocol_build_request(from_user) -> str:
    """
    build the request according to user selection and protocol
    return: string - msg code
    """
    
    print("protocol_build_request not implemented")
    return str()


def protocol_parse_reply(reply: bytes) :
    """
    parse the server reply and prepare it to user
    return: answer from server string
    """
    fields = reply.split(b'~')
    code = fields[0]
    if code == b'TURN':
        pass




if __name__ == "__main__":
    GUI("127.0.0.1")