class Wallet:
    def __init__(self, start_balance) -> None:
        self.balance = start_balance

    def deposit(self, value):
        print(f"{value} added to your balance")
        self.balance += value

    def withdraw(self, value):
        print(f"{value} taken from your balance")
        self.balance -= value
    
    def __str__(self) -> str:
        return f"Wallet Balance: {self.balance}"
