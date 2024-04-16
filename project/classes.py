import random


class Player:
    def __init__(self, color: str, name: str, addr: tuple) -> None:
        self.__color = color
        self.__name = name
        self.__addr = addr
        self.__pos = 0
        self.__double_streak = 0
        self.__money = 0

    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def play(self):
        dice1 = self.roll_dice()
        dice2 = self.roll_dice()

        if dice1 == dice2:
            self.__double_streak += 1
        else:
            self.__double_streak = 0

        self.__pos += dice1 + dice2
        card = self.get_card()

    def earn_or_pay(self, amount: int) -> None:
        # If amount positive player earn, if negative player pay
        self.__money += amount

    def get_color(self) -> str:
        return self.__color

    def set_color(self, color: str) -> None:
        self.__color = color

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_addr(self) -> tuple:
        return self.__addr

    def set_addr(self, addr: tuple) -> None:
        self.__addr = addr

    def get_pos(self) -> int:
        return self.__pos

    def set_pos(self, location: int) -> None:
        self.__pos = location

    def get_double_streak(self) -> int:
        return self.__double_streak

    def set_double_streak(self, double_streak: int) -> None:
        self.__double_streak = double_streak

    def get_money(self) -> int:
        return self.__money

    def set_money(self, money: int) -> None:
        self.__money = money


class Card:
    def __init__(self, pos: int, name: str) -> None:
        self.__pos = pos
        self.__name = name

    def get_position(self) -> int:
        return self.__pos

    def set_position(self, location: int) -> None:
        self.__pos = location

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name



class House(Card):
    def __init__(self, pos: int, name: str, purchase_price: int, rental_price: list[int]) -> None:
        super().__init__(pos, name)
        self.__price = purchase_price
        self.__rental = rental_price
        self.__owner: Player = None
        self.__house_count = 0
    
    def get_price(self) -> int:
        return self.__price

    def get_rental(self, houses_count: int = 0):
        return self.__rental[houses_count]
    
    def get_rental_list(self) -> list[int]:
        return self.__rental
    
    def set_owner(self,new_owner: Player):
        self.__owner = new_owner

    def get_owner(self) -> Player:
        return self.__owner


class SupriseCard():
    def __init__(self, description: str, result: str) -> None:
        # Result is the final outcome of the card. ex. (gain 50$, give to each player 20$ and so on)
        self.__description = description
        self.__result = result


class Suprise(Card):
    def __init__(self, pos: int, name: str) -> None:
        super().__init__(pos, name)
        self.__options: list[SupriseCard] = self.get_suprise_options()
    
    def draw_card(self) -> SupriseCard:
        return random.choice(self.__options)
        
    def get_suprise_options(self) -> list[SupriseCard]:
        # This initailze all the possible outcome from the suprise
        return []    
    
    


class Game:
    def __init__(self,players: list[Player] = []) -> None:
        self.__board: Board = Board()
        self.__players = players

    def do_move(self, player: Player, dice_result: int) -> None:
        # Move player, check what if it has to pay a player or something.
        pass

    def pay(self,from_:Player ,to: Player, amount: int) -> None:
        """from_ player loses money, to player earns.

        Args:

            amount (int): always positive
        """
        if amount > 0:
            from_.earn_or_pay(-amount)
            to.earn_or_pay(amount)
        else:
            raise ValueError("amount has to be positive, not ", amount)


class Board:
    def __init__(self,) -> None:
        self.__board: list[Card] = []
    
    def get_card_at_position(self,position: int) -> Card:
        return self.__board[position]
    
    def get_board(self) -> list[Card]:
        return self.__board

    def set_board(self, board: list[Card]) -> None:
        self.__board = board
