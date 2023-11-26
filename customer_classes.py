# Define customer classes
import threading
import time
import random
import names

class Customer:
    def __init__(self, id, casino):
        self.id = id
        self.gender = random.choice(["male", "female"])
        self.name = names.get_first_name(gender=self.gender)
        self.age = random.randint(16,80)
        self.bankroll = random.randint(0,9999999)
        self.start_bankroll = self.bankroll
        self.games_played = 0
        self.lock = threading.Lock()
        self.customer_type = "normal"
        self.entry_atts_ = {"drunkness":random.randint(1,8),
                            "rage":random.randint(1,8),
                            "is_vip": random.choices([True,False], weights=(10,90), k=1)[0],
                            "has_weapon": random.choices([True,False], weights=(10,90), k=1)[0]} 
        self.casino = casino
        self.min_bet_amount = 1

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
        at_the_door = True
        bouncer_found = False
        while at_the_door:
            print(f"{self.name} is waiting in line to enter the Casino")
            print(f"{self.name} is waiting for a bouncer")
            while not bouncer_found:
                for bouncer in self.casino.bouncers:
                    if bouncer.lock.locked():
                        time.sleep(2)
                        continue
                    bncr = bouncer
                    break
                bouncer_found = True
            entry = bncr.allow_entry(self)
            if not entry:
                return
            print(f"{self.name} has entered the casino.") 
            self.casino.customers.append(self) # Add self to casino list of customers
            at_the_door = False


        while True:
            # EXIT CONDITIONS

            # Exit condition 1
            if self.isBankrupt():
                break
            # Exit condition 2
            if (self.bankroll > (self.start_bankroll*1.75)) or (self.bankroll < (self.start_bankroll*0.25)):
                break
            # Exit condition 3
            if self.games_played > 10:
                break

            # SELECT AN ACTIVITY 
            task_id = random.choices(["play", "bar", "bathroom"], weights=(60,20,10), k=1)[0]
            
            # SELECT A TABLE TO GO PLAY AT
            # if task_id == "play":
            #     table_chosen = random.choices(self.casino.tables, weights=(60,20,10), k=1)[0]
            #     table_chosen.play() 
                # CAREFUL, not all tables have play method, some have play()
                                    #   add table_type attribute to table classes to identify which method to use
                                    #   or create a consistent method for all
            
            # BAR
            if task_id == "bar":
                at_the_bar = True
                unattended = True
                while at_the_bar:
                    while unattended:
                        print(f"{self.name} is waiting at the bar")
                        for bartender in self.casino.bartenders:
                            if bartender.lock.locked():
                                continue
                            brt = bartender
                            unattended = False
                    print(f"{self.name} is being attended by bartender {brt.name}")
                    brt.take_order(self)
                    drink = brt.make_drink()
                    brt.serve_drink(self)
                    print(f"{self.name} enjoys the {drink}.")
                    time.sleep(5)
                    at_the_bar = False
                continue

            # BATHROOM
            if task_id == "bathroom":
                self.goBathroom()
                continue          


class HighSpender(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.min_bet_amount = 100000
        self.customer_type = "high_spender"

    def enterVIP(self, time):
        print(f"Customer {self.name} has entered the VIP.")
        time.sleep(time)
        print(f"Customer {self.name} has left the VIP.")


class MediumSpender(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.min_bet_amount = 10000
        self.customer_type = "medium_spender"


class LowSpender(Customer):
    def __init__(self, id, casino):
        super().__init__(id, casino)
        self.min_bet_amount = 1000
        self.customer_type = "low_spender"

    

