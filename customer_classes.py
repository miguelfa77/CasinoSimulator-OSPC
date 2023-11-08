# Define customer classes
import threading
import time
import random

class Customer:
    def __init__(self, name, age, bankroll):
        self.name = name
        self.age = age
        self.bankroll = bankroll
        self.lock = threading.Lock()

    def bet(self, amount):    
        self.bankroll -= amount
        return amount
    
    def isBankrupt(self):
        return True if self.bankroll <= 0 else False
    
    def goBathroom(self):
        time.sleep(random.randrange(1, 20))


class HighSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount

    def bet(self, amount):
        with self.lock:
            print(f"Bet placed: {amount}")
            while amount < self.min_bet_amount:
                if amount < self.min_bet_amount:
                    print(f"Bet placed: {amount}")
                    print(f"That's not how we ride, increase that figure.")
                    amount *= 2
            print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
            self.bankroll -= amount

    def enterVIP(self, time):
        print(f"Customer {self.name} has entered the VIP.")
        time.sleep(time)
        print(f"Customer {self.name} has left the VIP.")



class MediumSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount

    def bet(self, amount):
        with self.lock:
            while amount < self.min_bet_amount:
                print(f"Bet placed: {amount}")
                if amount < self.min_bet_amount:
                    print(f"Bet does not meet required minimum amount, increasing bet...")
                    amount *= 2
                print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
            self.bankroll -= amount

class LowSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount

    def bet(self, amount):
        with self.lock:
            while amount < self.min_bet_amount:
                print(f"Bet placed: {amount}")
                if amount < self.min_bet_amount:
                    print(f"Bet does not meet required minimum amount, increasing bet...")
                    amount *= 2
                print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
            self.bankroll -= amount




        


