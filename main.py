import math
from blackjack import BlackJack, Result
from wallet import Wallet


def get_int_from_user(prompt, max_value=math.inf) -> int:
    while True:
        try:
            bet = int(input(prompt))
            if bet <= 0 or bet > max_value:
                print("Invalid Value")
                continue
            return bet
        except ValueError:
            bet = 0


def keep_playing() -> bool:
    while True:
        user_input = input("Keep Playing?(Y/N)")
        if user_input.upper().startswith("Y"):
            return True
        elif user_input.upper().startswith("N"):
            return False


bet_min = 2
bet_max = 500
game = BlackJack()
wallet = Wallet(get_int_from_user(
    "How many chips do you want to start with: "))


while True:
    bet = get_int_from_user("Bet Amount: ", max_value=wallet.balance)
    result = game.run_game()
    match result:
        case Result.PLAYER_WIN:
            print("You Win")
            wallet.deposit(bet)
        case Result.PLAYER_BLACKJACK:
            print("BLACKJACK!")
            wallet.deposit(2*bet)
        case Result.HOUSE_WIN | Result.HOUSE_BLACKJACK:
            print("Dealer Wins")
            wallet.withdraw(bet)
        case Result.TIE:
            print("Tie!")
            print("Everyone keeps their money")
    print(wallet)
    if wallet.balance == 0:
        print("Out of money")
        break

    if not keep_playing():
        break
