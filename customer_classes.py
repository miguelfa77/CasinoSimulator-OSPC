# Define customer classes
import threading
import time
import random
import names
from casino_class import Casino

class Customer:
    def __init__(self, customer_id=None):
        self.id = customer_id
        self.gender = random.choice("male", "female")
        self.name = names.get_full_name(gender=self.gender)
        self.age = random.randint(18,80)
        self.bankroll = random.randint(100000,9999999)
        self.lock = threading.Lock()

    def bet(self, amount):    
        self.bankroll -= amount
        return amount
    
    def isBankrupt(self):
        return True if self.bankroll <= 0 else False
    
    def goBathroom(self):
        time.sleep(random.randrange(1, 20))

    def run(self, casino):
        casino.customers.append(self)


class HighSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount

    def bet(self, amount, table): # ADD TABLE CONNECTION 
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

