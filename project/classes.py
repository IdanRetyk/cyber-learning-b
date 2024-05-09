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
                hand: tuple[Card,Card] | None = None
                ) -> None:

        self.__addr = addr
        self.__pos = position
        self.__hand: tuple[Card,Card] | None = hand
        self.__money = money
        self.__name = name
    
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
    
    def change_money(self, amount):
        self.__money += amount

    

class Game:
    def __init__(self,player_arr :list[Player] | None = None) -> None:
        if player_arr is None:
            player_arr = []
        self.__deck = CardDeck()
        self.__deck.shuffle()
        self.__community_cards: list[Card] = list() # The cards everyone can see
        self.__players: list[Player] = player_arr
        self.__pot: int = 0

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
    
    
    def get_players(self) -> list[Player]:
        return self.__players

    def get_community_cards(self):
        return self.__community_cards
    
    def change_pot(self,amount: int):
        self.__pot += amount
        
    def get_pot(self) -> int:
        return self.__pot
    
    
    
    def show_flop(self):
        for _ in range(3):
            self.__community_cards.append(self.__deck.draw_card())
    
    def show_turn(self):
        self.__community_cards.append(self.__deck.draw_card())
    
    def show_river(self):
        self.__community_cards.append(self.__deck.draw_card())
    
    def calculate_winners(self):
        raise NotImplementedError("Calculate winners not implemented")









if __name__ == "__main__":
    print("This file should not execute")