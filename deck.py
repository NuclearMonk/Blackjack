
from random import shuffle
from strenum import StrEnum
from typing import Deque, List, NamedTuple
from itertools import product
from collections import deque

class Suit(StrEnum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    
class Card(NamedTuple):
    rank: int
    suit: Suit
    
    def __str__(self) -> str:
        match self.rank:
            case 1:
                return f"A{self.suit.value}"
            case 11:
                return f"J{self.suit.value}"
            case 12:
                return f"Q{self.suit.value}"
            case 13:
                return f"K{self.suit.value}"
            case x:
                return f"{x}{self.suit.value}"         
class Deck:
    def __init__(self) -> None:
        self.cards : Deque[Card] = deque(Card(r,s) for s,r in product(Suit, range(1,14)))
        self.shuffle()

    def shuffle(self) -> None:
        shuffle(self.cards)
    
    def draw(self, count=1) -> List[Card]:
        return [self.cards.popleft() for _ in range(count)]