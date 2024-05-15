"""This file contains all general classes.

Card - (num,suit)
CardDeck - (deck)
Player - (addr,pos)
Game - (deck,community_cards,players)

"""
import pathlib
import random
import pygame
from PIL import Image
from platform import system
from treys import Card as tCard
from treys import Evaluator
#check if run on windows or mac



project_folder = str(pathlib.Path(__file__).parent.resolve())
sys = system()
if sys == "Darwin":
    PIC_FOLDER = project_folder + "/pictures/"
elif sys == "Windows":
    PIC_FOLDER = project_folder + r"\pictures" + "\\"
else:
    PIC_FOLDER = ""
    raise ValueError()



class Card:
    def __init__(self,num: int ,suit: str ) -> None:
        """

        Args:
            num (int): num is a number between 1 - 13 represting cards between A, 2, ..., 10, J, Q, K
            suit (str): one of four options - D, C, H, S
        
        Raises:
            ValueError, if the above condition aren't met
        """
        
        if num < 1 or num > 13:
            raise ValueError("Num value should be between 1,13 not " ,num)
        
        if suit not in ('D','C','H','S'):
            raise ValueError("Invalid suit - ", suit)
        
        self.__num = num
        self.__suit = suit

    def __repr__(self) -> str:
        return str(self.__num) + self.__suit

    def to_tCard(self) -> int:
        st_arr = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
        st = st_arr[self.__num - 1] + self.__suit.lower()
        return tCard.new(st)
        
    def get_suit(self) -> str:
        return self.__suit

    def get_num(self) -> int:
        return self.__num
    
    def get_picture(self) -> pygame.surface.Surface:
        im = Image.open(PIC_FOLDER + "deck.png")    
        
        top = ('S','C','D','H').index(self.__suit) * 59
        if (self.__suit == 'D'):
            top += 2
        if (self.__suit == 'H'):

            top += 4
        bottom = top + 59
        
        if (self.__num) == 1: # Ace
            left,right = 0,39
        else:
            left = (14 - self.__num) * 40 - 1
            right = left + 40
        if self.__num <= 5:
            left += 1
            right += 1


        
        im1 = im.crop((left,top,right,bottom))

        if im1.mode != "RGBA":
            im1 = im1.convert("RGBA")


        return pygame.image.fromstring(im1.tobytes(),im1.size,"RGBA")

class CardDeck:
    def __init__(self) -> None:
        self.__deck :list[Card] = []
        for i in range(1,14):
            self.__deck.append(Card(i,'S'))
            self.__deck.append(Card(i,'H'))
            self.__deck.append(Card(i,'D'))
            self.__deck.append(Card(i,'C'))
    
    
    def shuffle(self) -> None:
        """
        Shuffles deck in place
        """
        random.shuffle(self.__deck)
    
    def draw_card(self) -> Card:
        return self.__deck.pop()
    
    
class Player:
    def __init__(self,
                addr: tuple[str,int],
                position: int,
                money: int,
                name: str = "",
                hand: tuple[Card,Card] | None = None,
                ) -> None:

        self.__addr = addr
        self.__pos = position
        self.__hand: tuple[Card,Card] | None = hand
        self.__money = money
        self.__name = name
        self.__folded: bool = False
        self.__current_bet: int = 0
        
    def __repr__(self) -> str:
        return f" bet - {self.__current_bet}"
    
    
    def set_addr(self, addr: tuple[str,int]):
        self.__addr = addr
    
    def get_addr(self) -> tuple[str,int]:
        return self.__addr
    
    def set_position(self, position: int):
        self.__pos = position
    
    def get_position(self) -> int:
        return self.__pos
    
    def set_name(self, name: str):
        self.__name = name
    
    def get_name(self) -> str:
        return self.__name
    
    def set_hand(self, cards: tuple[Card,Card]):
        self.__hand = cards
    
    def get_hand(self) -> tuple[Card,Card]:
        if self.__hand is None:
            raise ValueError("Player cards are None")
        return self.__hand

    def set_money(self, money: int):
        self.__money = money
    
    def get_money(self) -> int:
        return self.__money
    
    def change_money(self, amount: int):
        self.__money += amount

    def fold(self):
        self.__folded = True
    
    def is_playing(self):
        return not self.__folded
    
    def get_curr_bet(self) -> int:
        return self.__current_bet
    
    def set_curr_bet(self,amount:int):
        self.__current_bet = amount
    
    # def get_hand_score(self,community_cards: list[Card]) -> tuple[int,Card]:
    #     """Considering player hole cards and the games community cards, return a score representing the best hand of this player.

    #     Straight flush - 0
    #     Four of a kind - 1
    #     Full house - 2
    #     Flush - 3
    #     Straight - 4
    #     Three of a kind - 5
    #     two pair - 6
    #     pair - 7
    #     high card - 8
        
    #     Args:
    #         community_cards (list[Card]): 5 cards.

    #     Returns:
    #         tuple[int,int]: first int according to the score table, second representing the kicker
    #     """
        
    #     card_list = list(self.__hand) + community_cards # type:ignore
    
    # @staticmethod
    # def straight_flush(cards):
        
    
    
    
class Game:
    def __init__(self,player_arr :list[Player] | None = None,blinds: tuple[int,int] = (5,10)) -> None:
        if player_arr is None:
            player_arr = []
        self.__deck = CardDeck()
        self.__deck.shuffle()
        self.__community_cards: list[Card] = list() # The cards everyone can see
        self.__players: list[Player] = player_arr
        self.__pot: int = 0
        self.__small_blind,self.__big_blind = blinds
        self.__bet_size: int = 0
        
        self.__deal_cards()
    
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_Game__deck']  # Remove the deck from the state
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
    
    def __deal_cards(self):
        """
        for every player in players, deal him to cards.
        """
        for player in self.__players:
            player.set_hand((self.__deck.draw_card(),self.__deck.draw_card()))
    
    
    def __repr__(self) -> str:
        return f"players - {self.__players}, pot - {self.__pot}"
    
    def get_winner(self) -> int:
        """Search for winner mid-game.
        a winner is the last player who hasn't folded yet.

        Returns:
            int: -1 if there is no winner yet. if there is a winner return index.
        """
        if self.players_in_game() != 1:
            return -1
        for i in range(len(self.__players)):
            if self.__players[i].is_playing():
                return i
        return -1
    
    def does_player_exist(self,addr):
        return addr in self.get_addresses_list()
    
    def players_in_game(self) -> int:
        return len(list(filter(Player.is_playing,self.__players)))
    
    
    def set_bet_size(self,size):
        self.__bet_size = size
        
    def get_bet_size(self) -> int:
        return self.__bet_size
    
    def get_players(self) -> list[Player]:
        return self.__players

    def get_community_cards(self):
        return self.__community_cards
    
    def change_pot(self,amount: int):
        self.__pot += amount
        
    def get_pot(self) -> int:
        return self.__pot
    
    def empty_pot(self) ->int:
        pot = self.__pot
        self.__pot = 0
        return pot
    
    def get_addresses_list(self) -> list[tuple[str,int]]:
        """return list of player's addresses"""
        return [p.get_addr() for p in self.__players]
    
    def show_flop(self):
        for _ in range(3):
            self.__community_cards.append(self.__deck.draw_card())
    
    def show_turn(self):
        self.__community_cards.append(self.__deck.draw_card())
    
    def show_river(self):
        self.__community_cards.append(self.__deck.draw_card())
    
    def calculate_winners(self) ->  list[int]:
        """Calculate best hand.

        Returns:
            list[int]: list of all the indexes with the best hand
        """
        eval = Evaluator()
        all_cards = [card.to_tCard() for card in list(self.__players[0].get_hand()) + self.__community_cards]
        best_hand = eval.evaluate(all_cards[:2],all_cards[2:]) 
        index_list = []
        for i in range(len(self.__players)):
            all_cards = [card.to_tCard() for card in list(self.__players[i].get_hand()) + self.__community_cards]
            curr_hand = eval.evaluate(all_cards[:2],all_cards[2:]) 
            if best_hand > curr_hand:
                best_hand = curr_hand
                index_list = [i]
            if best_hand == curr_hand and best_hand != 0:
                index_list.append(i)
        return list(set(index_list))
    
    def get_blind(self,big: bool | int) -> int:
        if big:
            return self.__big_blind
        else:
            return self.__small_blind









if __name__ == "__main__":
    print("This file should not execute")