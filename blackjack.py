from enum import Enum, auto
from time import sleep
from typing import List
from deck import Deck, Card
import os


class Result(Enum):
    PLAYER_WIN = auto()
    PLAYER_BLACKJACK = auto()
    HOUSE_WIN = auto()
    HOUSE_BLACKJACK = auto()
    TIE = auto()


class BlackJack:

    def __init__(self) -> None:
        self.__deck = Deck()
        self.__house_cards = []
        self.__player_cards = []

    def __get_card(self) -> Card:
        try:
            card, *_ = self.__deck.draw()
        except IndexError:
            self.__deck = Deck()
            card, *_ = self.__deck.draw()
        return card

    @staticmethod
    def __score(cards: List[Card]) -> int:
        """ Calculates the blackjack score of a given list of cards
            The rules for score calculation are as follows
            Number cards are worth their number
            Figure Cards are worth 10
            Aces are worth 11, if they cause a player to bust over 21, they are worth 1 instead
        Args:
            cards (List[Card]): List of card object that represents a hand

        Returns:
            int: The final score, a score above 21 means the player busted out
        """
        score = 0
        for card in cards:
            match card.rank:
                case 1:  # Case of ace
                    score += 11
                case 11 | 12 | 13:  # Case of figure cards
                    score += 10
                case x:  # General case
                    score += x
        if score <= 21:
            return score
        # if the player has busted we search for aces and count their value as 1, one at a time until either
        # the player is no longer busted or we run out of cards
        for card in cards:
            if card.rank == 1:
                score -= 10
                if score <= 21:
                    return score
        return score

    def __setup_round(self) -> None:
        """ Sets up a round where the player and the dealer each get 2 cards
        """
        self.__house_cards = []
        self.__player_cards = []
        self.__house_cards.append(self.__get_card())
        self.__player_cards.append(self.__get_card())
        self.__house_cards.append(self.__get_card())
        self.__player_cards.append(self.__get_card())

    def __hit_player(self):
        """Gives the player an extra card"""
        self.__player_cards.append(self.__get_card())

    def __hit_dealer(self) -> None:
        self.__house_cards.append(self.__get_card())

    def __check_winner(self) -> Result:
        match self.__score(self.__house_cards), self.__score(self.__player_cards):
            case dealer_score, _ if dealer_score > 21:
                return Result.PLAYER_WIN
            case _, player_score if player_score > 21:
                return Result.HOUSE_WIN
            case dealer_score, player_score if dealer_score > player_score:
                return Result.HOUSE_WIN
            case dealer_score, player_score if dealer_score == player_score:
                return Result.TIE
            case dealer_score, player_score if dealer_score < player_score:
                return Result.PLAYER_WIN

    @staticmethod
    def __hit_or_stay() -> bool:
        while True:
            user_input = input("Hit or Stay?(H/S)")
            if user_input.upper().startswith("H"):
                return True
            elif user_input.upper().startswith("S"):
                return False

    def __display_game_state(self, hide_dealer_card=True) -> None:
        sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        if hide_dealer_card:
            print("Dealer")
            print(
                "■■", *self.__house_cards[1:], f"({self.__score(self.__house_cards[1:])})")
            print()
            print()
            print(*self.__player_cards,
                  f"({self.__score(self.__player_cards)})")
            print("Player")
        else:
            print("Dealer")
            print(*self.__house_cards,
                  f"({self.__score(self.__house_cards)})")
            print()
            print()
            print(*self.__player_cards,
                  f"({self.__score(self.__player_cards)})")
            print("Player")

    @staticmethod
    def __end_screen(winner: Result) -> None:
        match winner:
            case Result.PLAYER_WIN:
                print("Player Wins!")
            case Result.HOUSE_WIN:
                print("House Wins!")
            case Result.TIE:
                print("TIE!")

    def run_game(self) -> None:
        self.__setup_round()
        self.__display_game_state()

        if (self.__score(self.__player_cards) == 21):
            self.__display_game_state(hide_dealer_card=False)
            return Result.PLAYER_BLACKJACK if self.__score(self.__house_cards) != 21 else Result.TIE
        elif (self.__score(self.__house_cards) == 21):
            self.__display_game_state(hide_dealer_card=False)
            return Result.HOUSE_BLACKJACK

        while self.__score(self.__player_cards) <= 21:
            if self.__hit_or_stay():
                self.__hit_player()
            else:
                break
            self.__display_game_state()
        else:
            self.__display_game_state()
            return Result.HOUSE_WIN
        self.__display_game_state(hide_dealer_card=False)
        while self.__score(self.__house_cards) < 17:
            self.__hit_dealer()
            self.__display_game_state(hide_dealer_card=False)
        winner = self.__check_winner()
        return winner
