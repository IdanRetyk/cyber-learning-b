import random
from PIL import Image


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

    def get_suit(self) -> str:
        return self.__suit

    def get_num(self) -> int:
        return self.__num
    
    def get_picture(self) -> Image.Image:
        # TODO should display the correct picture.
        raise NotImplementedError()


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
    def __init__(self,addr: tuple[str,int],position : int) -> None:
        self.__addr = addr
        self.__pos = position
    

class Game:
    def __init__(self,addr_arr: list[tuple[str,int]]) -> None:
        self.__deck = CardDeck()
        self.__deck.shuffle()
        self.__community_cards: list[Card] = [] # The cards everyone can see
        self.__players: list[Player]= []
        
        pos_count = 1
        for addr in addr_arr:
            self.__players.append(Player(addr,pos_count))
            pos_count += 1
        
        
        self.__deal_cards()
    
    def __deal_cards(self):
        pass
    
    def show_flop(self):
        for _ in range(3):
            self.__community_cards.append(self.__deck.draw_card())
    
    def show_turn(self):
        self.__community_cards.append(self.__deck.draw_card())
    
    def show_river(self):
        self.__community_cards.append(self.__deck.draw_card())

    def get_players_cards(self,cards: list[tuple[Card,Card]]):
        self.__player_cards = cards
    
    def calculate_winners(self):
        raise NotImplementedError("Calculate winners not implemented")