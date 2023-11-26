# Define customer classes
import threading
import time
import random
import names
from casino_class import Casino

class Customer:
    def __init__(self, id, casino):
        self.id = id
        self.gender = random.choice(["male", "female"])
        self.name = names.get_first_name(gender=self.gender)
        self.age = random.randint(16,80)
        self.bankroll = random.randint(0,9999999)
        self.lock = threading.Lock()
        self.customer_type = "normal"
        self.entry_atts_ = {"drunkness":random.randint(1,8),
                            "rage":random.randint(1,8),
                            "is_vip": random.choices([True,False], weights=(10,90), k=1)[0],
                            "has_weapon": random.choices([True,False], weights=(10,90), k=1)[0]} 
        self.casino = casino

    def bet(self, amount):    
        self.bankroll -= amount
        return amount
    
    def isBankrupt(self):
        return True if self.bankroll <= 0 else False
    
    def goBathroom(self):
        if self.gender == "male":
            if len(self.casino.bathrooms["Mens"]) < 5:
                with self.casino.bathrooms["mens_wc_lock"]:
                    self.casino.bathrooms["Mens"].append(self)
                    print(f"{self.name} is using the bathroom...")
                    time.sleep(random.randrange(1, 20))
                    self.casino.bathrooms["Mens"].remove(self)
                    print(f"{self.name} left the bathroom")
            else:
                print("Bathrooms are full, returning later.")
        if self.gender == "female":
            if len(self.casino.bathrooms["Womens"]) < 10:
                with self.casino.bathrooms["womens_wc_lock"]:
                    self.casino.bathrooms["Womens"].append(self)
                    print(f"{self.name} is using the bathroom...")
                    time.sleep(random.randrange(5, 20))
                    self.casino.bathrooms["Womens"].remove(self)
                    print(f"{self.name} left the bathroom")
            else:
                print("Bathrooms are full, returning later.")

    def leave(self):
        if self in self.casino.customers:
            with self.casino.locks["customers_lock"]:
                print(f"Customer {self.name} has left the casino.")
                self.casino.customers.remove(self)
        

    def run(self):
        print(f"{self.name} is waiting in line")
        for bouncer in self.casino.bouncers:
            while bouncer.lock.locked():
                print(f"Customer waiting for bouncer")
                time.sleep(2)
            print(f"{self.name} found bouncer")
            entry = bouncer.allow_entry(self)
            if not entry:
                break
            print(f"{self.name} has entered the casino.") 
            self.casino.customers.append(self) # Add self to casino list of customers


        # EXIT CASINO CONDITION
        # while True:
        #     if self.bankroll <= 0:
        #         break
            # SELECT A TABLE TO GO PLAY AT
            # PLAY AT TABLE
            # CHECK IF WINNING
            # CHANGE TABLE OR LEAVE
            # pass           


class HighSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount
        self.customer_type = "high_spender"

    def bet(self, amount, table): # ADD TABLE CONNECTION 
        with self.lock:
            print(f"Bet placed: {amount}")
            while amount < self.min_bet_amount:
                if amount < self.min_bet_amount:
                    amount *= 2
            print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
            self.bankroll -= amount
            table.pot += amount

    def enterVIP(self, time):
        print(f"Customer {self.name} has entered the VIP.")
        time.sleep(time)
        print(f"Customer {self.name} has left the VIP.")



class MediumSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount
        self.customer_type = "medium_spender"

    def bet(self, amount, table):
        with self.lock:
            while amount < self.min_bet_amount:
                print(f"Bet placed: {amount}")
                if amount < self.min_bet_amount:
                    print(f"Bet does not meet required minimum amount, increasing bet...")
                    amount *= 2
                print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
            self.bankroll -= amount
            table.pot += amount

class LowSpender(Customer):
    def __init__(self, name, age, bankroll, min_bet_amount):
        super().__init__(name, age, bankroll)
        self.min_bet_amount = min_bet_amount
        self.customer_type = "low_spender"

    def bet(self, amount, table): 
        with self.lock:
            while amount < self.min_bet_amount:
                print(f"Bet placed: {amount}")
                if amount < self.min_bet_amount:
                    print(f"Bet does not meet required minimum amount, increasing bet...")
                    amount *= 2
                print(f"{self.name} has placed a bet of {amount}, leaving them with a total of {self.bankroll} in their account.")
            self.bankroll -= amount
            table.pot += amount

